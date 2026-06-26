from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^\d{2}\d{8,9}$',
    message='Telefone deve estar no formato DDD + número, somente dígitos (ex: 21987654321).',
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, validators=[phone_validator])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
