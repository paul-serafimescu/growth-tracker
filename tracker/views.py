from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from api.guild import GuildManager
from .models import Guild

class Index(View):
  def get(self, request: HttpRequest) -> HttpResponse:
   return render(request, 'home.html', {})

class ServerListView(View):
  def get(self, request: HttpRequest) -> HttpResponse:
    context = {
      'guilds': (guilds := GuildManager(request.user.access_token).get_user_guilds()),
    }
    for guild in guilds:
      if guild['id'] not in [guild.guild_id for guild in Guild.objects.filter(guild_id__in=[g['id'] for g in guilds])]:
        Guild(name=guild['name'], guild_id=guild['id'], icon=guild['icon'], permissions=guild['permissions']).save()
    return render(request, 'guilds.html', context)

class ServerView(View):
  def get(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    try:
      context = {
        'guild': Guild.objects.get(guild_id=guild_id)
      }
    except ObjectDoesNotExist:
      return HttpResponseNotFound('<h1>not found</h1>')
    return render(request, 'guild.html', context)

  def patch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    return HttpResponse('testing...')
