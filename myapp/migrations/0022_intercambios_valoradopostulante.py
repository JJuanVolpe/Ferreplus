# Generated by Django 5.0.4 on 2024-06-11 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_rename_valorado_intercambios_valoradoempleado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambios',
            name='valoradoPostulante',
            field=models.BooleanField(default=False),
        ),
    ]
