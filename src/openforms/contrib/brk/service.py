from openforms.forms.models.form import Form
from openforms.plugins.exceptions import InvalidPluginConfiguration

from .checks import BRKValidatorCheck


def check_brk_config_for_addressNL() -> str:
    live_forms = Form.objects.live()

    if any(form.has_component("addressNL") for form in live_forms):
        try:
            BRKValidatorCheck.check_config()
        except InvalidPluginConfiguration as e:
            return e.args[0]

    return ""
