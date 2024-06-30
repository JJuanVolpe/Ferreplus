# Generated by Django 5.0.4 on 2024-06-30 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_alter_intercambios_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambios',
            name='valorCompra',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='status',
            field=models.CharField(default='NUEVO', max_length=200, null=True),
        ),
    ]
