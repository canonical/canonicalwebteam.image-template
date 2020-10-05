# Standard library
import unittest

# Local
from canonicalwebteam import image_template
from urllib.parse import quote


asset_url = (
    "https://assets.ubuntu.com/" "v1/479958ed-vivid-hero-takeover-kylin.jpg"
)
encoded_asset_url = quote(asset_url)
non_asset_url = (
    "https://dashboard.snapcraft.io/site_media/appmedia/"
    "2018/10/Screenshot_from_2018-10-26_14-20-14.png"
)
non_hostname_url = "/static/images/Screenshot_from_2018-10-26_14-20-14.png"


class TestImageTemplate(unittest.TestCase):
    def test_returns_string(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
        )
        self.assertTrue(isinstance(markup, str))

    def test_attributes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
            attrs={"id": "test", "title": "test title"},
        )
        self.assertIn('id="test"', markup)
        self.assertIn('title="test title"', markup)

    def test_classes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=False,
            attrs={"class": "test-title"},
        )
        # Check custom class exists
        self.assertIn('class="test-title"', markup)

    def test_optional_lazy(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            loading="auto",
            attrs={"class": "test-title"},
            hi_def=False,
        )
        # Check lazyload class is not present
        self.assertIn('class="test-title"', markup)

    def test_optional_fill(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            loading="auto",
            fill=True,
            hi_def=False,
        )
        # Check c_fill is present
        self.assertIn("c_fill", markup)

    def test_e_sharpen(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            loading="auto",
            fill=True,
            e_sharpen=True,
            hi_def=False,
        )
        # Check e_sharpen is present
        self.assertIn("e_sharpen", markup)

    def test_hi_def(self):
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=True,
        )
        markup_asset = image_template(
            url=asset_url, alt="test", width="1920", height="1080", hi_def=True
        )

        # Check the markup includes srcset
        self.assertTrue(markup.find("srcset="))
        self.assertTrue(markup.find("data-srcset"))
        # Check x2 is present
        self.assertTrue(markup.find("x2"))
        # Check width and height are double
        self.assertTrue(markup.find("3840"))
        self.assertTrue(markup.find("2160"))

        self.assertTrue(markup_asset.find("srcset="))
        self.assertTrue(markup_asset.find("data-srcset"))
        self.assertTrue(markup_asset.find("x2"))
        self.assertTrue(markup_asset.find("w%3D3840%26h%3D2160"))

    def test_height_is_optional(self):
        image = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
            hi_def=True,
        )

        self.assertNotIn("height=", image)
        self.assertNotIn("h_auto", image)


if __name__ == "__main__":
    unittest.main()
