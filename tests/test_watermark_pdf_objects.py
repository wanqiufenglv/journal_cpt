from __future__ import annotations

import unittest

from journal_cpt.processing.watermark import _form_has_configured_image, _xobject_dict


class NullIndirectObject:
    def get_object(self) -> object:
        return None

    def __getattr__(self, name: str) -> object:
        raise AttributeError(f"No attribute {name} found in IndirectObject or pointed object")


class IndirectObject:
    def __init__(self, value: object) -> None:
        self.value = value

    def get_object(self) -> object:
        return self.value


class WatermarkPdfObjectTests(unittest.TestCase):
    def test_xobject_dict_handles_null_indirect_resources(self) -> None:
        page = {"/Resources": NullIndirectObject()}

        self.assertEqual(_xobject_dict(page), {})

    def test_form_image_detection_skips_null_nested_xobjects(self) -> None:
        form = {
            "/Resources": {
                "/XObject": {
                    "/Broken": NullIndirectObject(),
                    "/WatermarkImage": IndirectObject({"/Subtype": "/Image", "/Width": 475, "/Height": 272}),
                }
            }
        }
        cfg = {"watermark": {"image_sizes": [[475, 272]]}}

        self.assertTrue(_form_has_configured_image(form, cfg))


if __name__ == "__main__":
    unittest.main()
