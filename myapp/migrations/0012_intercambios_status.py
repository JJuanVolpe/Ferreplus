# Generated by Django 5.0.4 on 2024-05-29 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_profile_sucursal'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambios',
            name='status',
            field=models.CharField(blank=True, default='NUEVO', max_length=200, null=True),
        ),
    ]
