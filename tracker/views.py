from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from .models import User, Server

class Index(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    print(User.objects.all())
    return HttpResponse('hi')

  def post(self, request: HttpRequest) -> HttpResponse:
    return HttpResponse('hi')
