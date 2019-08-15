# Standard library
import os
import sys
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode, quote

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(url, alt, width, height, hi_def, **attributes):
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

    if not url_parts.netloc:
        raise Exception("url must contain a hostname")

    std_def_cloudinary_options = cloudinary_options.copy()
    hi_def_cloudinary_options = cloudinary_options.copy()

    if not url_parts.netloc == "assets.ubuntu.com":
        std_def_cloudinary_options.append("w_" + str(width))
        std_def_cloudinary_options.append("h_" + str(height))

        if hi_def:
            hi_def_cloudinary_options.append("w_" + str(int(width) * 2))
            hi_def_cloudinary_options.append("h_" + str(int(height) * 2))
    elif url_parts.path[-4:] != ".svg":
        query = parse_qs(url_parts.query)

        if hi_def:
            query["w"] = int(width) * 2
            query["h"] = int(height) * 2
        else:
            query["w"] = int(width)
            query["h"] = int(height)

        url_list = list(url_parts)
        url_list[4] = urlencode(query, doseq=True)
        url = quote(urlunparse(url_list))

    # Split out classes from attributes
    # as we need to handle them specially
    extra_classes = None

    if "extra_classes" in attributes:
        extra_classes = attributes["extra_classes"]
        del attributes["extra_classes"]

    return template.render(
        url=url,
        alt=alt,
        std_def_cloudinary_options=",".join(std_def_cloudinary_options),
        hi_def_cloudinary_options=",".join(hi_def_cloudinary_options),
        width=int(width),
        height=int(height),
        hi_def=hi_def,
        extra_classes=extra_classes,
        attributes=attributes,
    )


sys.modules[__name__] = image_template
