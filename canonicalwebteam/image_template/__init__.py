# Standard library
import os
import sys
from urllib.parse import quote, unquote, urlparse

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")
cloudinary_url_base = "https://res.cloudinary.com/canonical/image/fetch"


def image_template(
    url,
    alt,
    width,
    height=None,
    fill=False,
    e_sharpen=False,
    loading="lazy",
    fmt="auto",
    attrs={},
    output_mode="html",
    sizes="(min-width: {}px) {}px, 100vw",
    srcset_widths=None,
    hi_def=False,
):
    """
    Generate responsive image markup with optimized srcset and sizes.

    Args:
        url: Image URL
        alt: Alt text for accessibility
        width: Primary image width
        height: Image height (optional)
        fill: Whether to crop and fill to exact dimensions
        e_sharpen: Whether to apply sharpening
        loading: Loading strategy ('lazy', 'auto')
        fmt: Image format ('auto', 'webp', 'jpg', etc.)
        attrs: Additional HTML attributes
        output_mode: 'html' or 'attrs'
        sizes: Responsive sizes attribute template
        srcset_widths: Custom widths for srcset generation
        hi_def: Enable high-DPI support (up to 2x)
    """

    url_parts = urlparse(url)

    # Default cloudinary optimisations
    # https://cloudinary.com/documentation/image_transformations
    cloudinary_options = [
        "f_" + str(fmt),
        "q_auto",  # Auto optimise quality
        "fl_sanitize",  # Sanitize SVG content
    ]

    if e_sharpen:
        cloudinary_options.append("e_sharpen")

    # If the original image does not match the requested
    # ratio set crop and fill see
    # https://cloudinary.com/documentation/image_transformation_reference#crop_parameter
    if fill:
        cloudinary_options.append("c_fill")

    if not url_parts.netloc:
        raise Exception("url must contain a hostname")

    std_def_cloudinary_options = cloudinary_options.copy()
    std_def_cloudinary_options.append("w_" + str(width))
    std_def_cloudinary_attrs = ",".join(std_def_cloudinary_options)

    # Decode the URL first to prevent double encoding
    decoded_url = unquote(url)
    encoded_url = quote(decoded_url, safe="")
    image_src = (
        f"{cloudinary_url_base}/"
        f"{std_def_cloudinary_attrs}/"
        f"{encoded_url}"
    )

    # Generate srcset values with optimized logic for real-world usage
    # https://vanillaframework.io/docs/settings/breakpoint-settings
    if srcset_widths is None:
        srcset_widths = [460, 620, 1036, 1681]

    width_int = int(width)
    srcset = []

    # Only generate srcset for images larger than 100px to avoid
    # unnecessary overhead
    if width_int > 100:
        max_srcset_width = max(srcset_widths)
        # When hi_def is enabled, allow slightly larger for high-DPI
        # But cap at 2x to avoid excessive payload
        if hi_def:
            max_width_limit = min(width_int * 2, max_srcset_width)
        else:
            max_width_limit = min(width_int, max_srcset_width)

        def create_srcset_url(width, options):
            width_options = options.copy()
            width_options.append(f"w_{width}")
            width_attrs = ",".join(width_options)
            return (
                f"{cloudinary_url_base}/{width_attrs}/"
                f"{encoded_url} {width}w"
            )

        # Generate srcset entries for standard widths
        filtered_widths = [w for w in srcset_widths if w <= max_width_limit]
        srcset.extend(
            create_srcset_url(w, cloudinary_options) for w in filtered_widths
        )

        # Add original width if needed
        existing_widths = {int(w) for w in filtered_widths}
        if width_int <= max_width_limit and width_int not in existing_widths:
            srcset.append(create_srcset_url(width_int, cloudinary_options))

    image_srcset = ", ".join(srcset)

    try:
        sizes = sizes.format(width, width)
    except (IndexError, KeyError):
        pass

    image_attrs = {
        "src": image_src,
        "srcset": image_srcset,
        "sizes": sizes,
        "alt": alt,
        "width": int(width),
        "height": height,
        "loading": loading,
        "attrs": attrs,
    }

    if not image_srcset:
        del image_attrs["srcset"]
        del image_attrs["sizes"]

    if output_mode == "html":
        return template.render(**image_attrs)
    elif output_mode == "attrs":
        merged_attrs = {**image_attrs, **attrs}
        del merged_attrs["attrs"]
        return merged_attrs
    else:
        raise ValueError("output_mode must be 'html' or 'attrs'")


sys.modules[__name__] = image_template
