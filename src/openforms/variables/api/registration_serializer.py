# The serializer is defined in a separate module to avoid circular imports.

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openforms.forms.api.serializers import FormVariableSerializer


class RegistrationPluginVariablesSerializer(serializers.Serializer):
    plugin_identifier = serializers.CharField(
        label=_("backend identifier"),
        help_text=_("The identifier of the registration plugin."),
    )
    plugin_verbose_name = serializers.CharField(
        label=_("backend verbose name"),
        help_text=_("The verbose name of the registration plugin."),
    )
    plugin_variables = serializers.ListSerializer(
        child=FormVariableSerializer(),
        label=_("variables"),
        help_text=_("The list of corresponding registration variables."),
    )
