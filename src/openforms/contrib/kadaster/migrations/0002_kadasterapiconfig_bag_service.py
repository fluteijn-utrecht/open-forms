# Generated by Django 3.2.21 on 2023-09-21 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("zgw_consumers", "0019_alter_service_uuid"),
        ("kadaster", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="kadasterapiconfig",
            name="bag_service",
            field=models.ForeignKey(
                help_text="Select which service to use for the BAG API.",
                limit_choices_to={"api_type": "orc"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="zgw_consumers.service",
                verbose_name="BAG service",
            ),
        ),
    ]