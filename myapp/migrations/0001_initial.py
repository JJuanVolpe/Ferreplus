# Generated by Django 5.0.4 on 2024-05-17 21:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='intercambios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('categoria', models.CharField(max_length=200)),
                ('foto', models.ImageField(upload_to='fotos_intercambios/')),
                ('descripcion', models.CharField(default='', max_length=200)),
                ('modelo', models.CharField(default='', max_length=200)),
                ('marca', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edad', models.PositiveBigIntegerField(null=True)),
                ('dni', models.CharField(max_length=10, null=True)),
                ('genero', models.CharField(blank=True, max_length=10, null=True)),
                ('telefono', models.CharField(blank=True, max_length=15, null=True)),
                ('Es_gerente', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
