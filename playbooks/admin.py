from django.contrib import admin

from .models import Playbook


@admin.register(Playbook)
class PlaybookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visibility', 'created_at')
    list_filter = ('visibility',)
    search_fields = ('title', 'description')
