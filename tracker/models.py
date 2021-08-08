from __future__ import annotations
from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
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
    return self.members

  def decrement_member_count(self) -> int:
    self.members -= 1
    self.save()
    return self.members

  @sync_to_async
  def async_save(self) -> None:
    self.save()

  class Meta:
    ordering = ['name']

class Snapshot(models.Model):
  url = models.UUIDField(default=uuid4, editable=False)
  guild = models.ForeignKey(Guild, on_delete=models.CASCADE)
  date = models.DateTimeField(auto_now_add=True)

  def __str__(self) -> str:
    return f'<{self.__class__.__name__} {self.url} : {self.guild}>'

  class Meta:
    ordering = ['date']
