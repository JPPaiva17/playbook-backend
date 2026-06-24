from django.conf import settings
from django.db import models

from plays.models import Play


class Playbook(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Público'
        PRIVATE = 'private', 'Privado'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playbooks',
    )
    plays = models.ManyToManyField(Play, blank=True, related_name='playbooks')
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
