# Standard library
import unittest

# Local
from canonicalwebteam import image_template


asset_url = (
    "https://assets.ubuntu.com/" "v1/479958ed-vivid-hero-takeover-kylin.jpg"
)
non_asset_url = (
    "https://dashboard.snapcraft.io/site_media/appmedia/"
    "2018/10/Screenshot_from_2018-10-26_14-20-14.png"
)
non_hostname_url = "/static/images/Screenshot_from_2018-10-26_14-20-14.png"


class TestImageTemplate(unittest.TestCase):
    def test_returns_string(self):
        markup = image_template(
            url=asset_url, alt="test", width="1920", height="1080"
        )
        self.assertTrue(isinstance(markup, str))

    def test_attributes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            attributes={"id": "test", "title": "test title"},
        )
        self.assertTrue(markup.find('id="test"') > -1)
        self.assertTrue(markup.find('title="test title"') > -1)

    def test_classes(self):
        markup = image_template(
            url=asset_url,
            alt="test",
            width="1920",
            height="1080",
            attributes={"class": "test-title"},
        )
        # Check custom class exists
        self.assertTrue(markup.find('class="test-title"') > -1)
        # Check lazyload class still exists
        self.assertTrue(markup.find('class="lazyload test-title"') > -1)

    def test_assets_url_has_width_and_height(self):
        markup_asset = image_template(
            url=asset_url, alt="test", width="1920", height="1080"
        )
        markup_non_asset = image_template(
            url=non_asset_url, alt="test", width="1920", height="1080"
        )
        self.assertTrue(asset_url + "?w=1920&h=1080" in markup_asset)
        self.assertTrue("w_1920" not in markup_asset)
        self.assertTrue("w_1920" in markup_non_asset)


if __name__ == "__main__":
    unittest.main()
