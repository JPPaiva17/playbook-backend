from django.contrib import admin

from .models import Play


@admin.register(Play)
class PlayAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visibility', 'players_required', 'created_at')
    list_filter = ('visibility', 'players_required')
    search_fields = ('title', 'description')
