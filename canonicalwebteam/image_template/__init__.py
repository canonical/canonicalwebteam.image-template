# Standard library
import os
import sys
from urllib.parse import urlparse

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(
    url,
    alt,
    hi_def,
    width,
    height=None,
    fill=False,
    e_sharpen=False,
    loading="lazy",
    attrs={},
):
    """
    Generate image markup
    """

    url_parts = urlparse(url)

    # Default cloudinary optimisations
    # https://cloudinary.com/documentation/image_transformations

    cloudinary_options = [
        "f_auto",  # Auto choose format
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
    hi_def_cloudinary_options = cloudinary_options.copy()

    std_def_cloudinary_options.append("w_" + str(width))

    if height is not None:
        std_def_cloudinary_options.append("h_" + str(height))

    if hi_def:
        hi_def_cloudinary_options.append("w_" + str(int(width) * 2))

        if height is not None:
            hi_def_cloudinary_options.append("h_" + str(int(height) * 2))

    return template.render(
        url=url,
        alt=alt,
        std_def_cloudinary_options=",".join(std_def_cloudinary_options),
        hi_def_cloudinary_options=",".join(hi_def_cloudinary_options),
        width=int(width),
        height=height,
        hi_def=hi_def,
        loading=loading,
        attrs=attrs,
    )


sys.modules[__name__] = image_template
