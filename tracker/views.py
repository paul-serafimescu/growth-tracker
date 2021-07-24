from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from .models import Server

class Index(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    return HttpResponse('hi')

  def post(self, request: HttpRequest) -> HttpResponse:
    return HttpResponse('hi')

class ServerListView(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    try:
      servers = Server.objects.all().filter(user=request.user)
    except ObjectDoesNotExist:
      servers = []
    return HttpResponse(servers)

class ServerView(View):
  def get(self, request: HttpRequest, server_name: str) -> HttpResponse:
    try:
      server: Server = Server.objects.all().filter(user=request.user).get(name=server_name)
    except ObjectDoesNotExist:
      server = "nope"
    return HttpResponse(server)
