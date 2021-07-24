from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from typing import Callable

class TokenVerification:
  def __init__(self, get_response: Callable):
    self.get_response = get_response

  def __call__(self, request: HttpRequest) -> HttpResponse:
    if isinstance(request.user, AbstractUser):
      if timezone.now() > request.user.expiration:
        logout(request)
        return redirect('/login')
    return self.get_response(request)
