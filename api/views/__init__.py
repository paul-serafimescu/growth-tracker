from rest_framework import routers
from .user import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
