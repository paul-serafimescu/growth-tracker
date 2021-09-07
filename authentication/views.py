from django.shortcuts import redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from tracker.models import DiscordUser
from config.environment import DISCORD_OAUTH_ROOT, DISCORD_API_ROOT, ENV
from config.exceptions import EnvKeyNotFoundError
from requests import post, get
from urllib.parse import quote
from discord_utils.guild import GuildManager
from tracker.models import Guild
from typing import Union, Any
from .util import ResponseParser, InvalidResponseError

class Login(View):
  def get(self, request: HttpRequest) -> HttpResponseRedirect:
    if request.user.is_authenticated:
      return redirect('/servers')
    if (client_id := ENV.get('CLIENT_ID')) is None:
      raise EnvKeyNotFoundError('CLIENT_ID')
    query_string = {
      'response_type': 'code',
      'client_id': client_id,
      'scope': [
        'identify',
        'guilds',
        'guilds.join',
        'email',
      ],
      'redirect_uri': quote('http://localhost:8000/accounts/authenticated')
    }
    return redirect(
      DISCORD_OAUTH_ROOT + 'authorize' + '?' + \
      '&'.join([f'{key}={value}' if not isinstance(value, list) \
        else '='.join((key, '%20'.join(value))) \
          for key, value in query_string.items()])
    )

class Logout(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
      logout(request)
    return HttpResponse('<p>logged out</p><p><a href="/">Login</a></p>')

class Authenticated(View):

  uri = 'http://localhost:8000/accounts/authenticated'

  if (client_secret := ENV.get('CLIENT_SECRET')) is None:
      raise EnvKeyNotFoundError('CLIENT_SECRET')

  if (client_id := ENV.get('CLIENT_ID')) is None:
    raise EnvKeyNotFoundError('CLIENT_ID')

  def fetch_token_json(self, code: str) -> dict[str, Union[str, int]]:
    data = {
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': self.uri
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    return post(DISCORD_OAUTH_ROOT + 'token', data=data, headers=headers).json()

  def fetch_user_info(self, token_type: str, token: str) -> dict[str, Any]:
    if token_type == 'BR':
      _token_type = 'Bearer'
    else:
      _token_type = 'Basic'
    headers = {
      'Authorization': f'{_token_type} {token}'
    }
    return get(DISCORD_API_ROOT + 'users/@me', headers=headers).json()

  def get(self, request: HttpRequest) -> HttpResponseRedirect:
    if (code := request.GET.get('code')) is None:
      return redirect('/accounts/login/')
    parser = ResponseParser(self.fetch_token_json(code))
    user_info = self.fetch_user_info(
      token_type := 'BR' if parser.get_or_raise('token_type') else 'BA',
      (access_token := parser.get_or_raise('access_token'))
    )
    expiration = timezone.now() + timezone.timedelta(0, parser.get_or_raise('expires_in'))
    if (id := user_info.get('id')) is None \
      or (username := user_info.get('username')) is None \
      or (email := user_info.get('email')) is None \
      or (discriminator := user_info.get('discriminator')) is None \
      or (avatar := user_info.get('avatar')) is None:
        raise InvalidResponseError()
    refresh_token = parser.get_or_raise('refresh_token')
    while (user := authenticate(request, username=f'{username} <{id}>', password=id)) is None: # user does not exist
      DiscordUser.objects.create_user(
        username=f'{username} <{id}>',
        password=str(id),
        email=email,
        access_token=access_token,
        token_type=token_type,
        expiration=expiration,
        refresh_token=refresh_token,
        discriminator=discriminator,
        avatar=avatar,
      )
    else: # user exists already, update token info
      user = authenticate(request, username=f'{username} <{id}>', password=str(id))
      user.access_token = access_token
      user.refresh_token = refresh_token
      user.expiration = expiration
      user.token_type = token_type
      user.email = email
      user.avatar = avatar
      user.discriminator = discriminator
      user.save()
    login(request, user)
    for guild in GuildManager(request.user.access_token).get_user_guilds():
      try:
        _guild = Guild.objects.get(guild_id=guild['id'])
        _guild.icon = guild['icon']
        _guild.name = guild['name']
        _guild.save()
      except:
        _guild = Guild.objects.create(
          guild_id=guild['id'],
          name=guild['name'],
          icon=guild['icon'],
        )
      _guild.users.add(request.user)
    return redirect('/')
