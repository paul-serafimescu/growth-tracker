from authentication.util import ResponseParser
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from api.refresh import Refresh, ResponseError
from datetime import datetime, timedelta
from typing import Callable

class TokenVerification:
  def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
    self.get_response = get_response

  def __call__(self, request: HttpRequest) -> HttpResponse:
    if isinstance(request.user, AbstractUser):
      if timezone.now() >= request.user.expiration:
        try:
          refreshed_token = Refresh(request.user.refresh_token)()
          parser = ResponseParser(refreshed_token)
          request.user.expiration = datetime.now() + timedelta(0, parser.get_or_raise('expires_in'))
          request.user.refresh_token = parser.get_or_raise('refresh_token')
          request.user.access_token = parser.get_or_raise('access_token')
          request.user.save()
        except ResponseError:
          logout(request)
          return redirect('/login')
    return self.get_response(request)
