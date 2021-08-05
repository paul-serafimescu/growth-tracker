from . import views
from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.Index.as_view()), name='index'),
    path('servers', login_required(views.ServerListView.as_view()), name='server-list'),
    path('servers/<str:guild_id>', login_required(views.ServerView.as_view()), name='server'),
]
