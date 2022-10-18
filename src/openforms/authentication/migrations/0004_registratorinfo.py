# Generated by Django 3.2.15 on 2022-10-17 14:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0060_auto_20220812_1439"),
        ("of_authentication", "0003_alter_authinfo_attribute"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegistratorInfo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "plugin",
                    models.CharField(
                        help_text="Identifier of the authentication plugin.",
                        max_length=250,
                        verbose_name="plugin",
                    ),
                ),
                (
                    "attribute",
                    models.CharField(
                        choices=[
                            ("bsn", "BSN"),
                            ("kvk", "KvK number"),
                            ("pseudo", "Pseudo ID"),
                            ("employee_id", "Employee ID"),
                        ],
                        help_text="Name of the attribute returned by the authentication plugin.",
                        max_length=50,
                        verbose_name="attribute",
                    ),
                ),
                (
                    "value",
                    models.CharField(
                        help_text="Value of the attribute returned by the authentication plugin.",
                        max_length=250,
                        verbose_name="value",
                    ),
                ),
                (
                    "attribute_hashed",
                    models.BooleanField(
                        default=False,
                        help_text="Are the auth/identifying attributes hashed?",
                        verbose_name="identifying attributes hashed",
                    ),
                ),
                (
                    "submission",
                    models.OneToOneField(
                        help_text="Submission related to this authentication information",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="_registrator",
                        to="submissions.submission",
                        verbose_name="Submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "Registrator authentication details",
                "verbose_name_plural": "Registrator authentication details",
            },
        ),
    ]
