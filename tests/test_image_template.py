# Standard library
import unittest

# Local
from canonicalwebteam import image_template
from urllib.parse import quote, unquote


asset_url = (
    "https://assets.ubuntu.com/" "v1/479958ed-vivid-hero-takeover-kylin.jpg"
)
non_asset_url = (
    "https://dashboard.snapcraft.io/site_media/appmedia/"
    "2018/10/Screenshot_from_2018-10-26_14-20-14.png"
)
non_hostname_url = "/static/images/Screenshot_from_2018-10-26_14-20-14.png"
cloudinary_url_base = "https://res.cloudinary.com/canonical/image/fetch"


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
        )
        # Check e_sharpen is present
        self.assertIn("e_sharpen", markup)

    def test_srcset(self):
        markup = image_template(
            url=non_asset_url, alt="test", width="1080", height="1080"
        )

        # Check the markup includes srcset (without hi_def, only up to
        # original width)
        self.assertIn("srcset=", markup)
        self.assertIn("460w", markup)
        self.assertIn("620w", markup)
        self.assertIn("1036w", markup)
        # Should not include (exceeds 1x without hi_def)
        self.assertNotIn("1386w", markup)

    def test_srcset_with_hi_def(self):
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
            height="1080",
            hi_def=True,
        )

        self.assertIn("srcset=", markup)
        self.assertIn("460w", markup)
        self.assertIn("620w", markup)
        self.assertIn("1036w", markup)
        self.assertIn("1681w", markup)

    def test_sizes(self):
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="540",
        )

        # Check the markup includes sizes
        self.assertIn('sizes="(min-width: 540px) 540px, 100vw"', markup)

    def test_custom_srcset_widths(self):
        custom_widths = [320, 640, 1280]
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="1000",
            srcset_widths=custom_widths,
            hi_def=True,
        )

        # Check the markup includes custom srcset widths within limits
        self.assertIn("srcset=", markup)
        self.assertIn("640w", markup)
        self.assertIn("1280w", markup)

    def test_custom_srcset_widths_without_hi_def(self):
        custom_widths = [320, 640, 1280]
        markup = image_template(
            url=non_asset_url,
            alt="test",
            width="1000",
            srcset_widths=custom_widths,
        )

        # Check the markup includes only widths up to 1x without hi_def
        self.assertIn("srcset=", markup)
        self.assertIn("320w", markup)
        self.assertIn("640w", markup)
        # Should not include (exceeds 1x without hi_def)
        self.assertNotIn("1280w", markup)
        # Should not include default widths that aren't in custom list
        self.assertNotIn("620w", markup)
        self.assertNotIn("1036w", markup)

    def test_no_srcset_for_small_images(self):
        # Test with image smaller than 100px threshold
        markup = image_template(url=non_asset_url, alt="test", width="80")

        self.assertNotIn("srcset=", markup)
        self.assertNotIn("sizes=", markup)

    def test_srcset_for_medium_images(self):
        # Test with image larger than 100px threshold
        markup = image_template(url=non_asset_url, alt="test", width="150")

        self.assertIn("srcset=", markup)
        self.assertIn("sizes=", markup)

    def test_height_is_optional(self):
        image = image_template(
            url=non_asset_url,
            alt="test",
            width="1920",
        )

        self.assertNotIn("height=", image)
        self.assertNotIn("h_1080", image)

    def test_attrs_return(self):
        image_attrs = {
            "url": asset_url,
            "alt": "test",
            "width": 1920,
            "height": 1080,
            "loading": "lazy",
            "attrs": {},
        }

        decoded_asset_url = unquote(asset_url)
        encoded_asset_url = quote(decoded_asset_url, safe="")

        returned_attrs = image_template(**image_attrs, output_mode="attrs")

        expected_attrs = image_attrs.copy()
        del expected_attrs["url"]
        del expected_attrs["attrs"]

        expected_attrs["src"] = (
            f"{cloudinary_url_base}/f_auto,q_auto,fl_sanitize,w_1920/"
            f"{encoded_asset_url}"
        )

        srcset_widths = [460, 620, 1036, 1681]
        srcset = []
        width = image_attrs["width"]

        max_width_limit = min(width, 1681)
        for srcset_width in srcset_widths:
            if srcset_width <= max_width_limit:
                srcset.append(
                    f"{cloudinary_url_base}/"
                    f"f_auto,q_auto,fl_sanitize,w_{srcset_width}/"
                    f"{encoded_asset_url} {srcset_width}w"
                )

        # Include original width if not already present and within limits
        if width <= max_width_limit and width not in [
            w for w in srcset_widths if w <= max_width_limit
        ]:
            srcset.append(
                f"{cloudinary_url_base}/"
                f"f_auto,q_auto,fl_sanitize,w_{width}/"
                f"{encoded_asset_url} {width}w"
            )

        expected_attrs["srcset"] = ", ".join(srcset)

        expected_attrs["sizes"] = f"(min-width: {width}px) {width}px, 100vw"

        self.assertEqual(expected_attrs, returned_attrs)


if __name__ == "__main__":
    unittest.main()
