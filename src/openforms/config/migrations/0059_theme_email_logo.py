# Generated by Django 4.2.11 on 2024-05-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0058_remove_globalconfiguration_enable_backend_formio_validation"),
    ]

    operations = [
        migrations.AddField(
            model_name="theme",
            name="email_logo",
            field=models.ImageField(
                blank=True,
                help_text="Upload the email logo, visible to users who receive an email. We advise dimensions around 150px by 75px. SVG's are not permitted.",
                upload_to="logo/",
                verbose_name="email logo",
            ),
        ),
    ]
