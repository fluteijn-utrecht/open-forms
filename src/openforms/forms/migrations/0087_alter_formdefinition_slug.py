# Generated by Django 3.2.20 on 2023-08-02 09:34

from django.db import migrations

import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0086_migrate_form_definition_slugs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="formdefinition",
            name="slug",
            field=autoslug.fields.AutoSlugField(
                editable=True, max_length=100, populate_from="name", verbose_name="slug"
            ),
        ),
    ]
