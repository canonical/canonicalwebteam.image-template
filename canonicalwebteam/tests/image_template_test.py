import unittest
import sys
from os.path import dirname, abspath
module_dir = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(module_dir)

from canonicalwebteam import image_template

class TestImageTemplate(unittest.TestCase):
    def test_returns_string(self):
        markup = image_template(
            path="/v1/479958ed-vivid-hero-takeover-kylin.jpg",
            alt="test",
            width="1920",
            height="1080"
        )
        self.assertTrue(isinstance(markup, str))

    def test_attributes(self):
        markup = image_template(
            path="/v1/479958ed-vivid-hero-takeover-kylin.jpg",
            alt="test",
            width="1920",
            height="1080",
            attributes={
                "id": "test",
                "title": "test title"
            }
        )
        self.assertTrue(
            markup.find('id="test"') > -1,
        )
        self.assertTrue(
            markup.find('title="test title"') > -1,
        )

    def test_classes(self):
        markup = image_template(
            path="/v1/479958ed-vivid-hero-takeover-kylin.jpg",
            alt="test",
            width="1920",
            height="1080",
            attributes={
                "class": "test-title"
            }
        )
        self.assertTrue(
            markup.find('class="test-title"') > -1,
        )


class TestAssetUrls(unittest.TestCase):
    def test_no_hostname_returns_assets_url(self):
        path = "/v1/479958ed-vivid-hero-takeover-kylin.jpg"
        markup = image_template(
            path=path,
            alt="test",
            width="1920",
            height="1080"
        )
        self.assertTrue(
            markup.find("https://assets.ubuntu.com" + path) > -1,
        )

    def test_assets_url_has_width_and_height(self):
        path = "/v1/479958ed-vivid-hero-takeover-kylin.jpg"
        markup = image_template(
            path=path,
            alt="test",
            width="1920",
            height="1080"
        )
        self.assertTrue(
            markup.find("https://assets.ubuntu.com" + path + "?w=1920&h=1080") > -1,
        )


class TestCustomUrls(unittest.TestCase):
    def test_no_hostname_returns_assets_url(self):
        path = "/v1/479958ed-vivid-hero-takeover-kylin.jpg"
        markup = image_template(
            path=path,
            alt="test",
            width="1920",
            height="1080"
        )
        self.assertTrue(
            markup.find(path) > -1,
        )


if __name__ == "__main__":
    unittest.main()
