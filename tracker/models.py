from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
  class Meta:
    ordering = ['username']

class Server(models.Model):
  name = models.CharField(max_length=100)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  class Meta:
    ordering = ['name']
