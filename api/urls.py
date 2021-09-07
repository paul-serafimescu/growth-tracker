from django.urls import include, path
from .views import router

urlpatterns = [
  path('/', include(router.urls)),
]
