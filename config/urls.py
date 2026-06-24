from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/plays/', include('plays.urls')),
    path('api/playbooks/', include('playbooks.urls')),
]
