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
    # Deprecated
    hi_def=False,
):
    """
    Generate image markup
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

    if height is not None:
        std_def_cloudinary_options.append("h_" + str(height))

    std_def_cloudinary_attrs = ",".join(std_def_cloudinary_options)
    image_src = f"{cloudinary_url_base}/{std_def_cloudinary_attrs}/{url}"

    # Generate srcset values
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-srcset
    srcset_widths = [
        320,
        480,
        640,
        800,
        1024,
        1280,
        1600,
        1920,
        2560,
    ]
    srcset = []
    for srcset_width in srcset_widths:
        if srcset_width <= int(width):
            srcset_options = cloudinary_options.copy()
            srcset_options.append("w_" + str(srcset_width))
            srcset_attrs = ",".join(srcset_options)
            srcset.append(
                f"{cloudinary_url_base}/{srcset_attrs}/{url} {srcset_width}w"
            )

    image_srcset = ", ".join(srcset)

    image_attrs = {
        "src": image_src,
        "srcset": image_srcset,
        "sizes": sizes.format(width, width),
        "alt": alt,
        "width": int(width),
        "height": height,
        "loading": loading,
        "attrs": attrs,
    }

    if output_mode == "html":
        return template.render(**image_attrs)
    elif output_mode == "attrs":
        merged_attrs = {**image_attrs, **attrs}
        del merged_attrs["attrs"]
        return merged_attrs
    else:
        raise ValueError("output_mode must be 'html' or 'attrs'")


sys.modules[__name__] = image_template
