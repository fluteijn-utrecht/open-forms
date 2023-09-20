import json
from dataclasses import dataclass

from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

import jq
from json_logic import jsonLogic

from openforms.forms.models import FormVariable
from openforms.typing import DataMapping, JSONObject, JSONValue
from openforms.variables.models import DataMappingTypes, ServiceFetchConfiguration


@dataclass
class FetchResult:
    value: JSONValue
    request_parameters: JSONObject
    response_json: JSONValue
    # zds Client returns json, we don't have access to
    # response_body: str  # base64 as services could return any bytearray
    # response_headers: JSONObject


sentinel = object()


def perform_service_fetch(
    var: FormVariable, context: DataMapping, submission_uuid: str = ""
) -> FetchResult:
    """Fetch a value from a http-service, perform a transformation on it and
    return the result.

    Form variables may receive their value from external (HTTP-based) services.
    For this a configuration object is required specifying the details on where
    and how to retrieve the data, and how to transform that data into something
    that can be stored in a form variable and be used in form fields and logic.
    The result is presented as a form variable value for a given submission
    instance.

    The value returned by the request is cached using the submission UUID and the
    arguments to the request (hashed to make a cache key).
    """

    if not var.service_fetch_configuration:
        raise ValueError(
            f"Can't perform service fetch on {var}. "
            "It needs a service_fetch_configuration."
        )
    fetch_config: ServiceFetchConfiguration = var.service_fetch_configuration

    client = fetch_config.service.build_client()
    request_args = fetch_config.request_arguments(context)

    if not submission_uuid:
        raw_value = client.request(**request_args)
    else:
        cache_key = hash(submission_uuid + json.dumps(request_args, sort_keys=True))

        raw_value = cache.get(cache_key, sentinel)
        if raw_value is sentinel:
            raw_value = client.request(**request_args)
            cache.set(
                cache_key,
                raw_value,
                timeout=fetch_config.cache_timeout
                if fetch_config.cache_timeout is not None
                else DEFAULT_TIMEOUT,
            )

    match fetch_config.data_mapping_type, fetch_config.mapping_expression:
        case DataMappingTypes.jq, expression:
            # XXX raise warning if len(result) > 1 ?
            value = jq.compile(expression).input(raw_value).first()
        case DataMappingTypes.json_logic, expression:
            value = jsonLogic(expression, raw_value)
        case _:
            value = raw_value

    return FetchResult(
        value=value,
        request_parameters=request_args,
        response_json=raw_value,
    )
