# Generated by Django 4.2.11 on 2024-04-12 08:43

from django.db import migrations

from openforms.translations.utils import get_language_codes


def add_extra_source_id_govmetric(apps, schema_editor):
    AnalyticsToolsConfiguration = apps.get_model(
        "analytics_tools", "AnalyticsToolsConfiguration"
    )

    config = AnalyticsToolsConfiguration.objects.first()
    if not config:
        return

    language_codes = get_language_codes()

    for language_code in language_codes:
        if old_id := getattr(config, f"govmetric_source_id_{language_code}"):
            setattr(config, f"govmetric_source_id_form_aborted_{language_code}", old_id)
            setattr(
                config, f"govmetric_source_id_form_finished_{language_code}", old_id
            )

        if old_guid := getattr(config, f"govmetric_secure_guid_{language_code}"):
            setattr(
                config, f"govmetric_secure_guid_form_aborted_{language_code}", old_guid
            )
            setattr(
                config, f"govmetric_secure_guid_form_finished_{language_code}", old_guid
            )

    config.save()


def remove_extra_source_id_govmetric(apps, schema_editor):
    AnalyticsToolsConfiguration = apps.get_model(
        "analytics_tools", "AnalyticsToolsConfiguration"
    )

    config = AnalyticsToolsConfiguration.objects.first()
    if not config:
        return

    language_codes = get_language_codes()

    for language_code in language_codes:
        new_id = getattr(
            config, f"govmetric_source_id_form_finished_{language_code}"
        ) or getattr(config, f"govmetric_source_id_form_aborted_{language_code}")
        if new_id:
            setattr(config, f"govmetric_source_id_{language_code}", new_id)

        new_guid = getattr(
            config, f"govmetric_secure_guid_form_finished_{language_code}"
        ) or getattr(config, f"govmetric_secure_guid_form_aborted_{language_code}")
        if new_guid:
            setattr(config, f"govmetric_secure_guid_{language_code}", new_guid)

    config.save()


class Migration(migrations.Migration):
    dependencies = [
        (
            "analytics_tools",
            "0008_analyticstoolsconfiguration_govmetric_secure_guid_form_abort_and_more",
        ),
    ]

    operations = [
        migrations.RunPython(
            add_extra_source_id_govmetric, remove_extra_source_id_govmetric
        ),
    ]
