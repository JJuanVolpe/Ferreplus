# Generated by Django 5.0.4 on 2024-05-19 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sucursal',
            name='address',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='city',
            field=models.CharField(default='', max_length=40, null=True),
        ),
    ]
