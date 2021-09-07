from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('tracker.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('authentication.urls')),
    path('api', include('api.urls')),
]
