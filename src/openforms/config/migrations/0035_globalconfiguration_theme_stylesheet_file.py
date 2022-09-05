# Generated by Django 3.2.15 on 2022-08-31 10:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0034_merge_20220816_1227"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="theme_stylesheet_file",
            field=models.FileField(
                blank=True,
                help_text="A stylesheet with theme-specific rules for your organization. This will be included as final stylesheet, overriding previously defined styles. If both a URL to a stylesheet and a stylesheet file have been configured, the uploaded file is included after the stylesheet URL.",
                upload_to="config/themes/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        allowed_extensions=("css",)
                    )
                ],
                verbose_name="theme stylesheet",
            ),
        ),
    ]