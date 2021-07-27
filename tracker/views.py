from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from api.guild import GuildManager
from .models import Guild

class Index(View):
  def get(self, request: HttpRequest) -> HttpResponse:
   return render(request, 'home.html', {})

  def post(self, request: HttpRequest) -> HttpResponse:
    return HttpResponse('hi')

class ServerListView(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    context = {
      'guilds': GuildManager(request.user.access_token).get_user_guilds(),
    }
    return render(request, 'guilds.html', context)
