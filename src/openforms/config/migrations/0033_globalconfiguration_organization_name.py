# Generated by Django 3.2.16 on 2022-12-07 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0032_auto_20221129_1241"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="organization_name",
            field=models.CharField(
                blank=True,
                help_text="The name of your organization that will be used as label for elements like the logo.",
                max_length=100,
                verbose_name="organization name",
            ),
        ),
    ]