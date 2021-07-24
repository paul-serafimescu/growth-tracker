from django.db import models
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

  class Meta:
    ordering = ['username']

class Server(models.Model):
  name = models.CharField(max_length=100)
  user = models.ForeignKey(DiscordUser, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.name

  class Meta:
    ordering = ['name']
