# Generated by Django 5.1.2 on 2024-11-03 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makoapp', '0006_property_property_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
