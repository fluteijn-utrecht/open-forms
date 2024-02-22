# Generated by Django 3.2.23 on 2024-01-22 16:14

import django.db.migrations.operations.special
import django.db.models.deletion
from django.db import migrations, models
from django.utils.module_loading import import_string

import openforms.forms.migration_operations


class Migration(migrations.Migration):

    dependencies = [
        ("forms", "0046_squashed_to_openforms_v230"),
        ("config", "0053_v230_to_v250"),
    ]

    operations = [
        migrations.AddField(
            model_name="form",
            name="activate_on",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time on which the form should be activated.",
                null=True,
                verbose_name="activate on",
            ),
        ),
        migrations.AddField(
            model_name="form",
            name="deactivate_on",
            field=models.DateTimeField(
                blank=True,
                help_text="Date and time on which the form should be deactivated.",
                null=True,
                verbose_name="deactivate on",
            ),
        ),
        # RunPython operations are removed, they were executed as part of the 2.5.0 upgrade.
        migrations.AddConstraint(
            model_name="formstep",
            constraint=models.UniqueConstraint(
                fields=("form", "form_definition"),
                name="form_form_definition_unique_together",
            ),
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "time", "move_time_validators"
        ),
        migrations.AddField(
            model_name="formstep",
            name="is_applicable",
            field=models.BooleanField(
                default=True,
                help_text="Whether the step is applicable by default.",
                verbose_name="is applicable",
            ),
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "textfield", "alter_prefill_default_values"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "date", "alter_prefill_default_values"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "datetime", "alter_prefill_default_values"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "postcode", "alter_prefill_default_values"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "bsn", "alter_prefill_default_values"
        ),
        migrations.AddField(
            model_name="form",
            name="theme",
            field=models.ForeignKey(
                blank=True,
                help_text="Apply a specific appearance configuration to the form. If left blank, then the globally configured default is applied.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="config.theme",
                verbose_name="form theme",
            ),
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "select", "set_openforms_datasrc"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "radio", "set_openforms_datasrc"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "selectboxes", "set_openforms_datasrc"
        ),
        # RunPython operations are removed, they were executed as part of the 2.5.0 upgrade.
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "columns", "fix_column_sizes"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "file", "fix_default_value"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "licenseplate", "ensure_validate_pattern"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "postcode", "ensure_validate_pattern"
        ),
        openforms.forms.migration_operations.ConvertComponentsOperation(
            "datetime", "prevent_datetime_components_from_emptying_invalid_values"
        ),
    ]
