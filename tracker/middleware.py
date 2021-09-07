from authentication.util import ResponseParser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.views import View
from django.contrib.auth.models import AbstractUser, AnonymousUser
from config.environment import BOT_CLIENT_TOKEN
from discord_utils.refresh import Refresh, ResponseError
from .models import Guild
from typing import Callable, Union

BOT_NOT_JOINED = 'bot did not join'
INVALID_DECORATOR = 'invalid decorator use'

class TokenVerification:
  def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
    self.get_response = get_response

  def __call__(self, request: HttpRequest) -> HttpResponse:
    if isinstance(request.user, AnonymousUser):
      return self.get_response(request)
    if isinstance(request.user, AbstractUser):
      if timezone.now() >= request.user.expiration:
        try:
          refreshed_token = Refresh(request.user.refresh_token)()
          parser = ResponseParser(refreshed_token)
          request.user.expiration = timezone.now() + timezone.timedelta(0, parser.get_or_raise('expires_in'))
          request.user.refresh_token = parser.get_or_raise('refresh_token')
          request.user.access_token = parser.get_or_raise('access_token')
          request.user.save()
        except ResponseError:
          logout(request)
          return redirect('/accounts/login')
    return self.get_response(request)

def protected_route(function: Callable[..., HttpResponse]) -> Union[Callable[..., HttpResponse], HttpResponse]:
  def wrapped(*args, **kwargs) -> Union[HttpResponse, None]:
    if not isinstance((request := args[1] if isinstance(args[0], View) else args[0]), HttpRequest):
      raise TypeError('invalid decorator use')
    if (authorization := request.headers.get('Authorization')) is None or authorization != BOT_CLIENT_TOKEN:
      return HttpResponse(status=405)
    return function(*args, **kwargs)
  return wrapped

def bot_joined(function: Callable[..., HttpResponse]) -> Union[Callable[..., HttpResponse], HttpResponse]:
  def wrapped(*args, **kwargs) -> Union[HttpResponse, None]:
    if not isinstance((request := args[1] if isinstance(args[0], View) else args[0]), HttpRequest):
      raise TypeError(INVALID_DECORATOR)
    try:
      if not (guild := get_object_or_404(Guild, guild_id=kwargs['guild_id'])).bot_joined:
        return HttpResponse(BOT_NOT_JOINED)
      request.guild = guild
    except (IndexError, KeyError):
      raise TypeError(INVALID_DECORATOR)
    retval = function(*args, **kwargs)
    del request.guild
    return retval
  return wrapped
