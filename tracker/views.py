from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View
from api.guild import GuildManager
from .models import Guild

class Index(View):
  def get(self, request: HttpRequest) -> HttpResponse:
   return render(request, 'home.html', {})

class ServerListView(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    context = {
      'guilds': GuildManager(request.user.access_token).get_user_guilds(),
    }
    return render(request, 'guilds.html', context)

class ServerView(View):
  def get(self, request: HttpRequest, guild_id: str) -> HttpResponse:
    return HttpResponse('hi')
