# Generated by Django 5.0.4 on 2024-05-29 22:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_profile_sucursal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intercambios',
            name='usuario',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='intercambios', to='myapp.profile'),
        ),
    ]