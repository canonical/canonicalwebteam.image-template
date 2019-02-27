# Standard library
import os
import sys
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(url, alt, width, height, attributes={}):
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

    if url_parts.netloc == "assets.ubuntu.com":
        # Use the assets server to resize the image
        # so we aren't caching more than we need in cloudinary

        query = parse_qs(url_parts.query)
        query["w"] = int(width)
        query["h"] = int(height)
        url_list = list(url_parts)
        url_list[4] = urlencode(query, doseq=True)
        url = urlunparse(url_list)
    else:
        # If not assets server, resize image on cloudinary
        cloudinary_options.append("w_" + str(width))
        cloudinary_options.append("h_" + str(height))

    # Split out classes from attributes
    # As we need to handle them specially
    extra_classes = None

    if "class" in attributes:
        extra_classes = attributes["class"]
        del attributes["class"]

    return template.render(
        url=url,
        alt=alt,
        cloudinary_options=",".join(cloudinary_options),
        width=int(width),
        height=int(height),
        extra_classes=extra_classes,
        attributes=attributes,
    )


sys.modules[__name__] = image_template
