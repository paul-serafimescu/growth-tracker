from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from tracker.models import DiscordUser
from rest_framework import serializers, viewsets

class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = DiscordUser
    fields = [
      'username',
      'discriminator',
      'avatar',
      'email'
    ]

class UserViewSet(viewsets.ModelViewSet):
  queryset = DiscordUser.objects.all()
  serializer_class = UserSerializer
