# Generated by Django 2.2.20 on 2021-06-03 13:13

from django.db import migrations, models

import openforms.submissions.models
import openforms.utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ("submissions", "0016_auto_20210521_1352"),
    ]

    operations = [
        migrations.AlterField(
            model_name="submission",
            name="bsn",
            field=models.CharField(
                blank=True,
                default=openforms.submissions.models.get_default_bsn,
                max_length=9,
                validators=[openforms.utils.validators.BSNValidator()],
                verbose_name="BSN",
            ),
        ),
    ]
