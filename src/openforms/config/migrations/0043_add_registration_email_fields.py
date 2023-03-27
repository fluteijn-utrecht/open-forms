# Generated by Django 3.2.18 on 2023-03-17 15:22

from django.db import migrations, models
import functools
import openforms.config.models
import openforms.emails.validators
import openforms.template.validators
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ("config", "0042_globalconfiguration_enable_service_fetch"),
    ]

    operations = [
        migrations.AddField(
            model_name="globalconfiguration",
            name="registration_email_content_html",
            field=tinymce.models.HTMLField(
                default=functools.partial(
                    openforms.config.models._render,
                    *("emails/email_registration_content.html",),
                    **{}
                ),
                help_text="Content of the registration email message (as HTML). Can be overridden on the form level.",
                validators=[
                    openforms.template.validators.DjangoTemplateValidator(
                        backend="openforms.template.openforms_backend"
                    ),
                    openforms.emails.validators.URLSanitationValidator(),
                ],
                verbose_name="registration email content HTML",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="registration_email_content_text",
            field=models.TextField(
                default=functools.partial(
                    openforms.config.models._render,
                    *("emails/email_registration_content.txt",),
                    **{}
                ),
                help_text="Content of the registration email message (as text). Can be overridden on the form level.",
                validators=[
                    openforms.template.validators.DjangoTemplateValidator(
                        backend="openforms.template.openforms_backend"
                    ),
                    openforms.emails.validators.URLSanitationValidator(),
                ],
                verbose_name="registration email content text",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="registration_email_payment_subject",
            field=models.CharField(
                default=functools.partial(
                    openforms.config.models._render,
                    *("emails/email_registration_subject_payment.txt",),
                    **{}
                ),
                help_text="Subject of the registration email message that is sent when the payment is received. Can be overridden on the form level.",
                max_length=1000,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="registration email payment subject",
            ),
        ),
        migrations.AddField(
            model_name="globalconfiguration",
            name="registration_email_subject",
            field=models.CharField(
                default=functools.partial(
                    openforms.config.models._render,
                    *("emails/email_registration_subject.txt",),
                    **{}
                ),
                help_text="Subject of the registration email message. Can be overridden on the form level.",
                max_length=1000,
                validators=[openforms.template.validators.DjangoTemplateValidator()],
                verbose_name="registration email subject",
            ),
        ),
    ]
