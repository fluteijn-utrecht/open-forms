# Generated by Django 3.2.17 on 2023-02-08 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0040_alter_globalconfiguration_favicon"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="clamav_host",
            field=models.CharField(
                blank=True,
                help_text="Hostname or IP address where ClamAV is running.",
                max_length=1000,
                verbose_name="ClamAV server hostname",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="clamav_port",
            field=models.IntegerField(
                blank=True,
                help_text="The TCP port on which ClamAV is listening.",
                null=True,
                verbose_name="ClamAV port number",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="clamav_timeout",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="ClamAV socket timeout expressed in seconds (optional).",
                null=True,
                verbose_name="ClamAV socket timeout",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="enable_virus_scan",
            field=models.BooleanField(
                default=False,
                help_text="Whether the files uploaded by the users should be scanned by ClamAV virus scanner.In case a file is found to be infected, the file is deleted.",
                verbose_name="Enable virus scan",
            ),
        ),
    ]
