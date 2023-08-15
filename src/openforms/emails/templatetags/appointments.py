from django import template
from django.template.loader import render_to_string

from openforms.appointments.models import Appointment
from openforms.appointments.renderer import AppointmentRenderer
from openforms.appointments.utils import get_plugin
from openforms.submissions.rendering.constants import RenderModes

register = template.Library()


@register.simple_tag(takes_context=True)
def appointment_information(context):
    # Use get since _appointment_id could be an empty string
    if not (appointment_id := context.get("_appointment_id")):
        return ""

    if as_text := context.get("rendering_text", False):
        template_name = "emails/templatetags/appointment_information.txt"
    else:
        template_name = "emails/templatetags/appointment_information.html"

    # check for new style appointments
    submission = context["_submission"]
    appointment: Appointment | None = getattr(submission, "appointment", None)
    plugin_id = appointment.plugin if appointment else ""

    plugin = get_plugin(plugin=plugin_id)

    tag_context = {
        "appointment": plugin.get_appointment_details(appointment_id),
        "appointment_renderer": AppointmentRenderer(
            submission=submission,
            mode=RenderModes.confirmation_email,
            as_html=not as_text,
        ),
        "appointment_cancel_link": plugin.get_cancel_link(context["_submission"]),
        "appointment_change_link": plugin.get_change_link(context["_submission"])
        if not appointment
        else "",
    }
    return render_to_string(template_name, tag_context)
