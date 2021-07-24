from django.shortcuts import render
from django.views import View
from django.http import HttpRequest, HttpResponse

class Profile(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    pass

