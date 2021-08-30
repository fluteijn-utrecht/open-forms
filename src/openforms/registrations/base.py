from typing import TYPE_CHECKING, Optional, Type

from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openforms.utils.mixins import JsonSchemaSerializerMixin

if TYPE_CHECKING:
    from openforms.submissions.models import Submission

SerializerCls = Type[serializers.Serializer]


class EmptyOptions(JsonSchemaSerializerMixin, serializers.Serializer):
    pass


class BasePlugin:
    verbose_name = _("Set the 'verbose_name' attribute for a human-readable name")
    """
    Specify the human-readable label for the plugin.
    """
    configuration_options: SerializerCls = EmptyOptions
    """
    A serializer class describing the plugin-specific configuration options.

    A plugin instance is the combination of a plugin callback and a set of options that
    are plugin specific. Multiple forms can use the same plugin with different
    configuration options. Using a serializer allows us to serialize the options as JSON
    in the database, and de-serialize them into native Python/Django objects when the
    plugin is called.
    """

    backend_feedback_serializer: Optional[SerializerCls] = None
    """
    A serializer class describing the plugin-specific backend feedback data.

    Plugins often interact with other backend systems that send response data. For
    debugging/troubleshooting purposes, this data can be stored as JSON using the
    specified serializer class.
    """

    is_demo_plugin = False

    def __init__(self, identifier: str):
        self.identifier = identifier

    def register_submission(
        self, submission: "Submission", options: dict
    ) -> Optional[dict]:
        raise NotImplementedError()

    def get_label(self):
        return self.verbose_name
