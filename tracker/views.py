from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from api.guild import GuildManager
from uuid import uuid4, UUID
from .middleware import protected_route
from .models import Guild, Snapshot

class Index(View):
  def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
   return render(request, 'home.html', {})

class ServerListView(View):
  def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
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
    # TODO: create Snapshot if one doesn't exist for today
    except ObjectDoesNotExist:
      return HttpResponseNotFound('<h1>not found</h1>')
    return render(request, 'guild.html', context)

  @protected_route
  def patch(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    guild: Guild = Guild.objects.get(guild_id=guild_id)
    if guild.members is None:
      return HttpResponse(status=200)
    guild.increment_member_count()
    return HttpResponse(status=200)

  @protected_route
  def post(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    # TODO: Snapshot creation protocol (only the bot can trigger a creation from this route)
    ...

class SnapShotView(View):
  def get(self, request: HttpRequest, ss_uuid: str, *args, **kwargs) -> HttpResponse:
    return HttpResponse(Snapshot.objects.get(url=ss_uuid).date)
