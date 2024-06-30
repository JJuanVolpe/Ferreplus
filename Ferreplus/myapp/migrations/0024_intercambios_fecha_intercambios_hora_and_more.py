# Generated by Django 5.0.4 on 2024-06-17 23:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_product_marca_product_modelo'),
    ]

    operations = [
        migrations.AddField(
            model_name='intercambios',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intercambios',
            name='hora',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='trueque_postulado',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='myapp.intercambios'),
        ),
    ]