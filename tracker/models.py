from __future__ import annotations
from django.db import models
from uuid import uuid4 as uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from config.environment import BASE_PATH
from asgiref.sync import sync_to_async
from typing import Any, Optional

def serializable(cls: type):
  def serialize(self) -> dict[str, Any]:
    return {key: value for key, value in self.__dict__.items() if not key.startswith('_')}
  if not hasattr(cls, serialize.__name__):
    setattr(cls, serialize.__name__, serialize)
  return cls

@serializable
class DiscordUser(AbstractUser):
  """ This user model is derived from the Discord OAuth 2.0 user object.

      The `username` field should be populated by Discord id, `password` field should be populated by `hash(username)`.
  """

  class TokenType(models.TextChoices):
    BASIC = 'BA', _('BASIC')
    BEARER = 'BR', _('BEARER')

  access_token = models.CharField(max_length=100)
  token_type = models.CharField(
    max_length=2,
    choices=TokenType.choices,
    default=TokenType.BEARER,
  )
  expiration = models.DateTimeField()
  refresh_token = models.CharField(max_length=100)
  avatar = models.CharField(max_length=40, null=True)
  discriminator = models.CharField(max_length=4, default='0001')

  def __str__(self) -> str:
    return self.username

  def __repr__(self) -> str:
    return self.__str__()

  @staticmethod
  def create_user(*args, **kwargs) -> DiscordUser:
    return DiscordUser.objects.create(**kwargs)

  def serialize(self) -> dict[str, Any]:
    return {
      'id': self.id,
      'username': ' '.join((split_username := self.username.split())[:-1]),
      'discord_id': split_username[-1][1:-1],
      'avatar':  self.avatar,
      'discriminator': self.discriminator,
    }

  class Meta:
    ordering = ['username']

@serializable
class Guild(models.Model):
  name = models.CharField(max_length=100)
  guild_id = models.CharField(max_length=30, unique=True)
  icon = models.CharField(max_length=100, null=True)
  members = models.IntegerField(null=True)
  users = models.ManyToManyField(DiscordUser)
  bot_joined = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def create_guild(*args, **kwargs) -> Guild:
    return Guild.objects.create(**kwargs)

  def increment_member_count(self, members: Optional[int]) -> int:
    if self.members is None:
      return
    if members is not None:
      self.members = members
    else:
      self.members += 1
    self.save()
    Snapshot.objects.create(guild=self, member_count=self.members)
    return self.members

  def decrement_member_count(self, members: Optional[int]) -> int:
    if self.members is None:
      return
    if members is not None:
      self.members = members
    else:
      self.members -= 1
    self.save()
    Snapshot.objects.create(guild=self, member_count=self.members)
    return self.members

  @sync_to_async
  def async_save(self) -> None:
    self.save()

  @sync_to_async
  def leave(self) -> None:
    self.bot_joined = False
    self.save()

  class Meta:
    ordering = ['name']

@serializable
class Snapshot(models.Model):
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  date = models.DateTimeField(default=timezone.localtime)
  member_count = models.IntegerField()

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} : {self.guild}>'

  class Meta:
    ordering = ['date']

@serializable
class Graph(models.Model):
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  url = models.UUIDField(default=uuid, editable=False)
  graph = models.FilePathField(path=BASE_PATH.joinpath('graphs').__str__())
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} : {self.guild}>'

  class Meta:
    ordering = ['date']
