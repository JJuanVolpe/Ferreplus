# Generated by Django 5.0.4 on 2024-05-31 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_intercambios_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('estado', models.CharField(max_length=200)),
                ('categoria', models.CharField(max_length=200)),
                ('foto', models.ImageField(upload_to='static/fotos_intercambios/')),
                ('descripcion', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
