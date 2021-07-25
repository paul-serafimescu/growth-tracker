from tracker.models import DiscordUser
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from config.environment import DISCORD_OAUTH_ROOT, DISCORD_API_ROOT, ENV
from config.exceptions import EnvKeyNotFoundError
from requests import post, get
from urllib.parse import quote
from typing import Union, Any
from .util import ResponseParser, InvalidResponseError
from datetime import datetime, timedelta

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
    return HttpResponse('logged out')

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
    headers = {
      'Authorization': f'{token_type} {token}'
    }
    return get(DISCORD_API_ROOT + 'users/@me', headers=headers).json()

  def get(self, request: HttpRequest) -> HttpResponseRedirect:
    if (code := request.GET.get('code')) is None:
      return redirect('/accounts/login/')
    parser = ResponseParser(self.fetch_token_json(code))
    user_info = self.fetch_user_info(
      (token_type := parser.get_or_raise('token_type')),
      (access_token := parser.get_or_raise('access_token'))
    )
    expiration = datetime.now() + timedelta(0, parser.get_or_raise('expires_in'))
    if (id := str(user_info.get('id'))) is None:
      raise InvalidResponseError()
    while (user := authenticate(request, username=id, password=id)) is None:
      DiscordUser.objects.create_user(
        username=id,
        password=id,
        access_token=access_token,
        token_type='BR' if token_type == 'Bearer' else 'BA',
        expiration=expiration,
        refresh_token=parser.get_or_raise('refresh_token')
      )
    login(request, user)
    return redirect('/')
