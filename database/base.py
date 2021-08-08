from asgiref.sync import sync_to_async
from .exceptions import ConnectionError
from config.environment import BASE_PATH
from typing import Union

import os
import django
import discord

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growth_tracker.settings')
django.setup()

from tracker.models import Guild, DiscordUser, Snapshot

class DatabaseMeta(type):
  """ why does python have to be like this
  """
  def __new__(cls, name, bases, dct):
    instance = super().__new__(cls, name, bases, dct)
    instance._instances = 0
    return instance

class Database(metaclass=DatabaseMeta):
  def __new__(cls, *args, **kwargs):
    return super(Database, cls).__new__(cls)

  def __init__(self) -> None:
    if Database._instances > 0:
      raise ConnectionError('multiple client connections to database not permitted')
    Database._instances = 1

  @sync_to_async
  def convert_guild_objects(self, guilds: discord.Guild) -> list[Guild]:
    return list(Guild.objects.filter(guild_id__in=[str(guild.id) for guild in guilds]))

  @sync_to_async
  def fetch_all_guilds(self) -> list[Guild]:
    return list(Guild.objects.all())

  @sync_to_async
  def fetch_guild_snapshots(self, guild: Guild) -> list[Snapshot]:
    return list(Snapshot.objects.filter(guild=guild))

  @sync_to_async
  def fetch_guild(self, **kwargs) -> Union[Guild, None]:
    try:
      return Guild.objects.get(**kwargs)
    except:
      return None

  @sync_to_async
  def add_guild_member(self, guild_id: str) -> int:
    return Guild.objects.get(guild_id=guild_id).increment_member_count()

  @sync_to_async
  def remove_guild_member(self, guild_id: str) -> int:
    return Guild.objects.get(guild_id=guild_id).decrement_member_count()
