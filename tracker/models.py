from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

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
    default=TokenType.BEARER
  )
  expiration = models.DateTimeField()
  refresh_token = models.CharField(max_length=100)

  def __str__(self) -> str:
    return self.username

  class Meta:
    ordering = ['username']

class Guild(models.Model):
  name = models.CharField(max_length=100)
  guild_id = models.CharField(max_length=30)
  icon = models.CharField(max_length=100)
  permissions = models.CharField(max_length=30)

  def __str__(self) -> str:
    return self.name

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
