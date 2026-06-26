import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(
                default='',
                max_length=11,
                validators=[
                    django.core.validators.RegexValidator(
                        message='Telefone deve estar no formato DDD + número, somente dígitos (ex: 21987654321).',
                        regex='^\\d{2}\\d{8,9}$',
                    )
                ],
            ),
            preserve_default=False,
        ),
    ]
