from . import views
from django.urls import re_path, path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    re_path(r'^$', login_required(views.Index.as_view()), name='index'),
    path('servers', login_required(views.ServerListView.as_view()), name='server-list'),
    path('server/<str:server_name>', login_required(views.ServerView.as_view()), name='server'),
]
