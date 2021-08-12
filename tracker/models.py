from __future__ import annotations
from django.db import models
from uuid import uuid4 as uuid
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from config.environment import BASE_PATH
from asgiref.sync import sync_to_async

class DiscordUser(AbstractUser):
  """ This user model is derived from the Discord OAuth 2.0 user object.

      The `username` field should be populated by Discord id, `password` field should be populated by `hash(id)`.
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

  def __str__(self) -> str:
    return self.username

  def __repr__(self) -> str:
    return self.__str__()

  @staticmethod
  def create_user(*args, **kwargs) -> DiscordUser:
    return DiscordUser.objects.create(**kwargs)

  class Meta:
    ordering = ['username']

class Guild(models.Model):
  name = models.CharField(max_length=100)
  guild_id = models.CharField(max_length=30, unique=True)
  icon = models.CharField(max_length=100, null=True)
  permissions = models.CharField(max_length=30)
  members = models.IntegerField(null=True)

  def __str__(self) -> str:
    return self.name

  @staticmethod
  def create_guild(*args, **kwargs) -> Guild:
    return Guild.objects.create(**kwargs)

  def increment_member_count(self) -> int:
    self.members += 1
    self.save()
    Snapshot.objects.create(guild=self, member_count=self.members)
    return self.members

  def decrement_member_count(self) -> int:
    self.members -= 1
    self.save()
    Snapshot.objects.create(guild=self, member_count=self.members)
    return self.members

  @sync_to_async
  def async_save(self) -> None:
    self.save()

  class Meta:
    ordering = ['name']

class Snapshot(models.Model):
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  date = models.DateTimeField(default=timezone.localtime)
  member_count = models.IntegerField()

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} : {self.guild}>'

  class Meta:
    ordering = ['date']

class Graph(models.Model):
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  url = models.UUIDField(default=uuid, editable=False)
  graph = models.FilePathField(path=BASE_PATH.joinpath('graphs').__str__())
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} : {self.guild}>'

  class Meta:
    ordering = ['date']
