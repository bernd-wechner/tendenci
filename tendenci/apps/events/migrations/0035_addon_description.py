# Generated by Django 4.2.14 on 2024-08-15 11:21

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0034_addon_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='addon',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]