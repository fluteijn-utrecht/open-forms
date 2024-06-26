import logging
from copy import deepcopy

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import SuspiciousOperation

from glom import PathAccessError, glom
from mozilla_django_oidc_db.mixins import SoloConfigMixin
from mozilla_django_oidc_db.utils import obfuscate_claim_value

from .models import (
    OpenIDConnectDigiDMachtigenConfig,
    OpenIDConnectEHerkenningBewindvoeringConfig,
    OpenIDConnectEHerkenningConfig,
    OpenIDConnectPublicConfig,
)

logger = logging.getLogger(__name__)


class SoloConfigDigiDMixin(SoloConfigMixin):
    config_class = OpenIDConnectPublicConfig


class SoloConfigEHerkenningMixin(SoloConfigMixin):
    config_class = OpenIDConnectEHerkenningConfig


class SoloConfigDigiDMachtigenMixin(SoloConfigMixin):
    config_class = OpenIDConnectDigiDMachtigenConfig


class SoloConfigEHerkenningBewindvoeringMixin(SoloConfigMixin):
    config_class = OpenIDConnectEHerkenningBewindvoeringConfig


class MachtigenBackendMixin:
    def get_or_create_user(self, access_token, id_token, payload):
        claims_verified = self.verify_claims(payload)
        if not claims_verified:
            msg = "Claims verification failed"
            raise SuspiciousOperation(msg)

        self.extract_claims(payload)

        user = AnonymousUser()
        user.is_active = True
        return user

    def extract_claims(self, payload: dict) -> None:
        self.request.session[self.session_key] = {}
        for claim_name in self.claim_names:
            self.request.session[self.session_key][claim_name] = glom(
                payload, claim_name
            )

    def log_received_claims(self, claims: dict):
        copied_claims = deepcopy(claims)

        def _obfuscate_claims_values(claims_to_obfuscate: dict) -> dict:
            for key, value in claims_to_obfuscate.items():
                if isinstance(value, dict):
                    _obfuscate_claims_values(value)
                else:
                    claims_to_obfuscate[key] = obfuscate_claim_value(value)
            return claims_to_obfuscate

        obfuscated_claims = _obfuscate_claims_values(copied_claims)
        logger.debug("OIDC claims received: %s", obfuscated_claims)

    def verify_claims(self, claims: dict) -> bool:
        self.log_received_claims(claims)

        for expected_claim in self.claim_names:
            try:
                glom(claims, expected_claim)
            except PathAccessError:
                logger.error(
                    "`%s` not in OIDC claims, cannot proceed with eHerkenning bewindvoering authentication",
                    expected_claim,
                )
                return False

        return True
