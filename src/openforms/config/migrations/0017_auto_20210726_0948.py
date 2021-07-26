# Generated by Django 2.2.24 on 2021-07-26 07:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0016_load_default_cookiegroups'),
    ]

    operations = [
        migrations.AddField(
            model_name='globalconfiguration',
            name='admin_session_timeout',
            field=models.PositiveIntegerField(default=60, help_text='Amount of time in minutes the admin can be inactive for before being logged out', validators=[django.core.validators.MinValueValidator(5)], verbose_name='admin session timeout'),
        ),
        migrations.AddField(
            model_name='globalconfiguration',
            name='form_session_timeout',
            field=models.PositiveIntegerField(default=60, help_text='Amount of time in minutes a user filling in a form can be inactive for before being logged out', validators=[django.core.validators.MinValueValidator(5)], verbose_name='form session timeout'),
        ),
    ]
