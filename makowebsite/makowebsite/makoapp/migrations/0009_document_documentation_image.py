# Generated by Django 5.1.2 on 2024-11-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('makoapp', '0008_document_documentation_file_delete_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='documentation_image',
            field=models.ImageField(blank=True, null=True, upload_to='document_images/'),
        ),
    ]