from authentication.util import ResponseParser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.views import View
from django.contrib.auth.models import AbstractUser
from config.environment import BOT_CLIENT_TOKEN
from api.refresh import Refresh, ResponseError
from typing import Callable, Union

class TokenVerification:
  def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
    self.get_response = get_response

  def __call__(self, request: HttpRequest) -> HttpResponse:
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
          return redirect('/login')
    return self.get_response(request)

def protected_route(function: Callable[..., HttpResponse]) -> Union[Callable[..., HttpResponse], HttpResponse]:
  def wrapped(*args, **kwargs) -> Union[HttpResponse, None]:
    if not isinstance((request := args[1] if isinstance(args[0], View) else args[0]), HttpRequest):
      raise TypeError('invalid decorator use')
    if (authorization := request.headers.get('Authorization')) is None or authorization != BOT_CLIENT_TOKEN:
      return HttpResponse(status=405)
    return function(*args, **kwargs)
  return wrapped
