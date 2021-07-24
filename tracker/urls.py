from . import views
from django.urls import re_path
from django.contrib.auth.decorators import login_required

urlpatterns = [
    re_path(r'^$', login_required(views.Index.as_view()), name='index'),
]
