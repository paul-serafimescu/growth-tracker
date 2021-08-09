from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime
from api.guild import GuildManager
from uuid import uuid4, UUID
from .middleware import protected_route
from .models import Guild, Snapshot

class WeekDaysMeta(type):
  def __new__(cls, *args, **kwargs) -> type:
    instance = super().__new__(cls, *args, **kwargs)
    instance.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return instance

class WeekDays(metaclass=WeekDaysMeta):
  def __init__(self, value: int) -> None:
    assert -1 < value < 7 and isinstance(value, int)
    self._value_ = value

  def __str__(self) -> str:
    return self.__class__.days[self._value_]

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
      guild = Guild.objects.get(guild_id=guild_id)
      snapshots = \
        {day:
          [snapshot for snapshot in
            Snapshot.objects.filter(guild__guild_id=guild_id, date__gte=timezone.now() - timezone.timedelta(days=30)) if str(WeekDays(snapshot.date.weekday())) == day]
        for day in WeekDays.days}
      context = {
        'guild': guild,
        'snapshots': snapshots,
      }
    except ObjectDoesNotExist:
      return HttpResponseNotFound('<h1>not found</h1>')
    return render(request, 'guild.html', context)

  @protected_route
  def patch(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    try:
      guild: Guild = Guild.objects.get(guild_id=guild_id)
    except ObjectDoesNotExist:
      return HttpResponse(status=404)
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
