from django.test import SimpleTestCase

from ...typing import Component
from .helpers import extract_error, validate_formio_data


class MapValidationTests(SimpleTestCase):

    def test_map_field_required_validation(self):
        component: Component = {
            "type": "map",
            "key": "foo",
            "label": "Test",
            "validate": {"required": True},
        }

        invalid_values = [
            ({}, "required"),
            ({"foo": ""}, "not_a_list"),
            ({"foo": None}, "null"),
        ]

        for data, error_code in invalid_values:
            with self.subTest(data=data):
                is_valid, errors = validate_formio_data(component, data)

                self.assertFalse(is_valid)
                self.assertIn(component["key"], errors)
                error = extract_error(errors, component["key"])
                self.assertEqual(error.code, error_code)

    def test_map_field_min_max_length_of_items(self):
        component: Component = {
            "type": "map",
            "key": "foo",
            "label": "Test",
        }

        invalid_values = [
            ({"foo": [34.869343]}, "min_length"),
            ({"foo": [34.869343, 24.080053, 24.074657]}, "max_length"),
        ]

        for data, error_code in invalid_values:
            with self.subTest(data=data):
                is_valid, errors = validate_formio_data(component, data)

                self.assertFalse(is_valid)
                self.assertIn(component["key"], errors)
                error = extract_error(errors, component["key"])
                self.assertEqual(error.code, error_code)
