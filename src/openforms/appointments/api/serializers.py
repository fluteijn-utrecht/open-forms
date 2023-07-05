from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from openforms.forms.models import Form

from ..base import BasePlugin
from ..utils import get_plugin
from .fields import ProductIDField


class AppointmentOptionsSerializer(serializers.Serializer):
    # TODO: validate that appointments cannot be enabled if there's no plugin configured
    is_appointment = serializers.BooleanField(
        label=_("Is appointment form"),
        help_text=_(
            "Boolean indicating if the form is an appointment form, using the new flow."
        ),
    )
    supports_multiple_products = serializers.SerializerMethodField(
        label=_("Multiple products supported?"),
        help_text=_(
            "If not supported, only one product/service can be booked at once and the "
            "UI may not allow the user to select multiple products."
        ),
    )

    @cached_property
    def _appointment_plugin(self) -> BasePlugin | None:
        try:
            return get_plugin()
        except ValueError:  # appointments plugin is not configured
            return None

    def get_supports_multiple_products(self, obj: Form) -> bool | None:
        # not an appointment -> don't bother looking up plugin configuration
        if not obj.is_appointment:
            return None
        plugin = self._appointment_plugin
        return plugin.supports_multiple_products if plugin else None


class ProductSerializer(serializers.Serializer):
    code = serializers.CharField(label=_("code"), help_text=_("Product code"))
    identifier = serializers.CharField(
        label=_("identifier"), help_text=_("ID of the product")
    )
    name = serializers.CharField(label=_("name"), help_text=_("Product name"))

    class Meta:
        ref_name = "AppointmentProduct"


class LocationSerializer(serializers.Serializer):
    identifier = serializers.CharField(
        label=_("identifier"), help_text=_("ID of the location")
    )
    name = serializers.CharField(label=_("name"), help_text=_("Location name"))


class LocationInputSerializer(serializers.Serializer):
    product_id = serializers.CharField(
        label=_("product ID"), help_text=_("ID of the product to get locations for")
    )


class DateInputSerializer(serializers.Serializer):
    product_id = serializers.CharField(
        label=_("product ID"), help_text=_("ID of the product to get dates for")
    )
    location_id = serializers.CharField(
        label=_("location ID"), help_text=_("ID of the location to get dates for")
    )


class DateSerializer(serializers.Serializer):
    date = serializers.DateField(label=_("date"))


class TimeInputSerializer(serializers.Serializer):
    product_id = serializers.CharField(
        label=_("product ID"), help_text=_("ID of the product to get times for")
    )
    location_id = serializers.CharField(
        label=_("location ID"), help_text=_("ID of the location to get times for")
    )
    date = serializers.DateField(label=_("date"), help_text=_("Date to get times for"))


class TimeSerializer(serializers.Serializer):
    time = serializers.DateTimeField(label=_("time"))


class CancelAppointmentInputSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label=_("email"), help_text=_("Email given when making the appointment")
    )


class CustomerFieldsInputSerializer(serializers.Serializer):
    product_id = ProductIDField(
        help_text=_("ID of the product to get required fields for")
    )
