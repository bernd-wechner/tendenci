# Generated by Django 4.2.13 on 2024-07-17 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regions', '0004_region_tax_label_2_region_tax_rate_region_tax_rate_2_and_more'),
        ('profiles', '0022_remove_profile_region_alter_profile_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='regions.region'),
        ),
    ]
