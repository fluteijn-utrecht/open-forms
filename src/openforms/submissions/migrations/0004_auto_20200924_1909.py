# Generated by Django 2.2.16 on 2020-09-24 17:09

import uuid

import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0002_delete_formsubmission"),
        ("submissions", "0003_auto_20200924_1710"),
    ]

    operations = [
        migrations.RenameField(
            model_name="submission",
            old_name="submitted_on",
            new_name="created_on",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="data",
        ),
        migrations.RemoveField(
            model_name="submission",
            name="form_name",
        ),
        migrations.AddField(
            model_name="submission",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AlterField(
            model_name="submission",
            name="form",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="forms.Form"
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="SubmissionStep",
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
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "data",
                    django.contrib.postgres.fields.jsonb.JSONField(
                        blank=True, null=True
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                (
                    "form_step",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="forms.FormStep"
                    ),
                ),
                (
                    "submission",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="submissions.Submission",
                    ),
                ),
            ],
            options={
                "verbose_name": "SubmissionStep",
                "verbose_name_plural": "SubmissionSteps",
            },
        ),
    ]
