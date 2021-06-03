from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import ugettext_lazy as _

from django_better_admin_arrayfield.models.fields import ArrayField
from solo.models import SingletonModel


class GlobalConfiguration(SingletonModel):
    email_template_netloc_allowlist = ArrayField(
        models.CharField(max_length=1000),
        verbose_name=_("allowed email domain names"),
        help_text=_(
            "Provide a list of allowed domains (without 'https://www')."
            "Hyperlinks in a (confirmation) email are removed, unless the "
            "domain is provided here."
        ),
        blank=True,
        default=list,
    )

    # for testing purposes!
    default_test_bsn = models.CharField(
        _("default test BSN"),
        default="",
        max_length=9,
        help_text=_(
            "When provided, submissions that are started will have this BSN set as "
            "default for the session. Useful to test/demo prefill functionality."
        ),
    )

    class Meta:
        verbose_name = _("General configuration")

    def __str__(self):
        return force_str(self._meta.verbose_name)
