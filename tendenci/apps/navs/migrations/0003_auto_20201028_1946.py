# Generated by Django 2.2.16 on 2020-10-28 19:46

from django.db import migrations, models
import tendenci.apps.base.validators


class Migration(migrations.Migration):

    dependencies = [
        ('navs', '0002_auto_20200902_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nav',
            name='title',
            field=models.CharField(max_length=100, validators=[tendenci.apps.base.validators.UnicodeNameValidator()]),
        ),
    ]
