from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from api.refresh import Refresh, ResponseError
from typing import Callable

class TokenVerification:
  def __init__(self, get_response: Callable):
    self.get_response = get_response

  def __call__(self, request: HttpRequest) -> HttpResponse:
    if isinstance(request.user, AbstractUser):
      if timezone.now() > request.user.expiration:
        try:
          refreshed_token = Refresh(request.user.refresh_token)()
          print(refreshed_token)
        except ResponseError:
          logout(request)
          return redirect('/login')
    return self.get_response(request)
