from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlayViewSet

router = DefaultRouter()
router.register('', PlayViewSet, basename='play')

urlpatterns = [
    path('', include(router.urls)),
]
