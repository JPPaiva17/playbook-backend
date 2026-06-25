from django.conf import settings
from django.db import models


class Play(models.Model):
    class Visibility(models.TextChoices):
        PUBLIC = 'public', 'Público'
        PRIVATE = 'private', 'Privado'

    class Map(models.TextChoices):
        MIRAGE = 'mirage', 'Mirage'
        INFERNO = 'inferno', 'Inferno'
        DUST2 = 'dust2', 'Dust 2'
        NUKE = 'nuke', 'Nuke'
        OVERPASS = 'overpass', 'Overpass'
        ANCIENT = 'ancient', 'Ancient'
        ANUBIS = 'anubis', 'Anubis'
        VERTIGO = 'vertigo', 'Vertigo'
        TRAIN = 'train', 'Train'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField()
    visibility = models.CharField(
        max_length=10,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )
    map = models.CharField(
        max_length=20,
        choices=Map.choices,
        blank=True,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='plays',
    )

    video_url = models.URLField(blank=True, null=True)

    players_required = models.PositiveSmallIntegerField(default=1)

    smokes = models.PositiveSmallIntegerField(default=0, verbose_name='Smokes')
    flashbangs = models.PositiveSmallIntegerField(default=0, verbose_name='Flashbangs')
    he_grenades = models.PositiveSmallIntegerField(default=0, verbose_name='HE Grenades')
    molotovs = models.PositiveSmallIntegerField(default=0, verbose_name='Molotovs/Incendiárias')
    decoys = models.PositiveSmallIntegerField(default=0, verbose_name='Decoys')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
