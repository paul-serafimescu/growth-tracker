from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
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
    context = {
      'guilds': list(request.user.guild_set.all()),
    }
    return render(request, 'home.html', context)

class ServerListView(View):
  def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
    context = {
      'guilds': list(request.user.guild_set.all()),
    }
    return render(request, 'guilds.html', context)

class ServerView(View):
  def get(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    def to_locale(snapshot: Snapshot) -> Snapshot:
      snapshot.date = timezone.localtime(snapshot.date)
      return snapshot

    try:
      context = {
        'guild': Guild.objects.get(guild_id=guild_id),
        'guilds': list(request.user.guild_set.all()),
        'snapshots': {day:
          [snapshot for snapshot in
            list(map(to_locale, Snapshot.objects.filter(guild__guild_id=guild_id, date__gte=timezone.now() - timezone.timedelta(days=7)))) if str(WeekDays(snapshot.date.weekday())) == day]
        for day in WeekDays.days},
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

class GraphView(View):
  def get(self, request: HttpRequest, guild_id: str, *args, **kwargs) -> HttpResponse:
    guild = get_object_or_404(Guild, guild_id=guild_id)
    if not guild.bot_joined:
      return HttpResponse('bot did not join')
    return JsonResponse(list(map(lambda snapshot : snapshot.serialize(), guild.snapshot_set.all())), safe=False)

