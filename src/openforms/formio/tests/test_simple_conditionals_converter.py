from django.test import SimpleTestCase, tag

from openforms.typing import JSONObject

from ..migration_converters import convert_simple_conditionals


class RegressionTests(SimpleTestCase):

    @tag("gh-4247")
    def test_editgrid_reference(self):
        configuration: JSONObject = {
            "components": [
                {
                    "type": "editgrid",
                    "key": "ingeschrevenOnderneming",
                    "label": "Gegevens onderneming",
                    "components": [
                        {
                            "type": "radio",
                            "key": "rechtsvorm",
                            "label": "Wat is de rechtsvorm van uw onderneming?",
                            "values": [
                                {
                                    "label": "Eenmanszaak / ZZP",
                                    "value": "EENMANSZAAK_ZZP",
                                },
                                {
                                    "label": "Vennootschap Onder Firma (VOF)",
                                    "value": "VENNOOTSCHAP_ONDER_FIRMA_VOF",
                                },
                                {
                                    "label": "Commanditaire Vennootschap (CV)",
                                    "value": "COMMANDITAIRE_VENNOOTSCHAP_CV",
                                },
                                {
                                    "label": "Besloten Vennootschap (BV)",
                                    "value": "BESLOTEN_VENNOOTSCHAP_BV",
                                },
                                {"label": "Maatschap", "value": "MAATSCHAP"},
                                {
                                    "label": "Stichting (met winstoogmerk)",
                                    "value": "STICHTING_MET_WINSTOOGMERK",
                                },
                            ],
                        },
                        {
                            "type": "number",
                            "key": "aantalVennoten",
                            "label": "Hoeveel vennoten heeft uw onderneming?",
                            "conditional": {
                                "eq": "VENNOOTSCHAP_ONDER_FIRMA_VOF",
                                "show": True,
                                "when": "ingeschrevenOnderneming.rechtsvorm",
                            },
                        },
                    ],
                }
            ]
        }

        try:
            convert_simple_conditionals(configuration)
        except Exception as exc:
            raise self.failureException("Unexpected crash") from exc
