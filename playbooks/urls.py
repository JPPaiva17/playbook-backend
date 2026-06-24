from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PlaybookViewSet

router = DefaultRouter()
router.register('', PlaybookViewSet, basename='playbook')

urlpatterns = [
    path('', include(router.urls)),
]
