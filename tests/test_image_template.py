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

    def test_small_images_generate_2x_srcset(self):
        """Test that small images (≤460px) generate 2x srcset"""
        html_result = image_template(
            url="https://example.com/image.jpg",
            alt="Test Image",
            width="50",
            height="50",
        )

        # Should contain srcset with 2x version
        self.assertIn("srcset", html_result)
        self.assertIn("100w", html_result)  # 2x the original 50px width

        attrs_result = image_template(
            url="https://example.com/image.jpg",
            alt="Test Image",
            width="50",
            height="50",
            output_mode="attrs",
        )

        # Should have srcset with 2x version
        self.assertIn("srcset", attrs_result)
        self.assertIn("100w", attrs_result["srcset"])

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

        srcset_widths = [460, 620, 1036, 1681, 1920]
        srcset = []
        width = image_attrs["width"]

        max_width_limit = min(width, 1920)
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

    # GIF handling removed as requested

    def test_webp_avif_use_cloudinary_with_srcset(self):
        # Test that WebP and AVIF files use Cloudinary
        # with format preservation and srcset
        test_cases = [
            ("https://example.com/image.webp", "f_webp"),
            ("https://example.com/image.avif", "f_avif"),
        ]

        for test_url, expected_format in test_cases:
            with self.subTest(url=test_url, format=expected_format):
                # Test attrs output for easier assertion
                attrs_result = image_template(
                    url=test_url,
                    alt="Test Image",
                    width="500",
                    height="300",
                    output_mode="attrs",
                )

                # Should use Cloudinary URL with format preservation
                self.assertIn("res.cloudinary.com", attrs_result["src"])
                self.assertIn(expected_format, attrs_result["src"])
                self.assertIn("q_auto", attrs_result["src"])
                self.assertIn("fl_sanitize", attrs_result["src"])
                self.assertIn("w_500", attrs_result["src"])

                # Should have srcset for images > 100px
                self.assertIn("srcset", attrs_result)
                self.assertIn("res.cloudinary.com", attrs_result["srcset"])
                self.assertIn(expected_format, attrs_result["srcset"])

                # Should have sizes attribute
                self.assertIn("sizes", attrs_result)

    def test_webp_avif_with_fill_and_sharpen(self):
        """Test that WebP and AVIF files respect fill and sharpen parameters"""
        test_url = "https://example.com/image.webp"

        attrs_result = image_template(
            url=test_url,
            alt="Test Image",
            width="400",
            height="200",
            fill=True,
            e_sharpen=True,
            output_mode="attrs",
        )

        # Should include fill and sharpen in both src and srcset
        self.assertIn("c_fill", attrs_result["src"])
        self.assertIn("e_sharpen", attrs_result["src"])
        self.assertIn("c_fill", attrs_result["srcset"])
        self.assertIn("e_sharpen", attrs_result["srcset"])

    def test_svg_uses_cloudinary_with_f_svg(self):
        """Test that SVGs use Cloudinary with f_svg format and no srcset"""
        svg_url = "https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg"

        # Test HTML output
        html_result = image_template(
            url=svg_url, alt="Test SVG", width="200", height="100"
        )

        # Should use Cloudinary with f_svg
        self.assertIn("res.cloudinary.com", html_result)
        self.assertIn("f_svg", html_result)
        self.assertIn("fl_sanitize", html_result)
        self.assertIn("w_200", html_result)
        self.assertNotIn("srcset", html_result)

        # Test attrs output
        attrs_result = image_template(
            url=svg_url,
            alt="Test SVG",
            width="200",
            height="100",
            output_mode="attrs",
        )

        # Should have Cloudinary URL with f_svg
        self.assertIn("res.cloudinary.com", attrs_result["src"])
        self.assertIn("f_svg", attrs_result["src"])
        self.assertIn("fl_sanitize", attrs_result["src"])
        self.assertIn("w_200", attrs_result["src"])
        self.assertEqual(attrs_result["alt"], "Test SVG")
        self.assertEqual(attrs_result["width"], 200)
        self.assertEqual(attrs_result["height"], "100")
        self.assertEqual(attrs_result["loading"], "lazy")
        self.assertNotIn("srcset", attrs_result)

    def test_svg_with_fill_and_sharpen(self):
        """Test that SVG files respect fill and e_sharpen parameters"""
        svg_url = "https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg"

        attrs_result = image_template(
            url=svg_url,
            alt="Test SVG",
            width="200",
            height="100",
            fill=True,
            e_sharpen=True,
            output_mode="attrs",
        )

        # Should include fill and sharpen parameters
        self.assertIn("c_fill", attrs_result["src"])
        self.assertIn("e_sharpen", attrs_result["src"])
        self.assertIn("f_svg", attrs_result["src"])


if __name__ == "__main__":
    unittest.main()
