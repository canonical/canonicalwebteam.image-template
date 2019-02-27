# Standard library
import os
import sys
from urllib.parse import urlparse, parse_qs, urlencode

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(path, alt, width, height, attributes={}):
    """
    Generate image markup
    """

    parse_result = urlparse(path)
    hostname=  parse_result.netloc
    if not hostname:
        hostname = "https://assets.ubuntu.com/"

        query = parse_qs(parse_result.query)
        query["w"] = int(width)
        query["h"] = int(height)
        path = hostname + parse_result.path.lstrip("/") + "?" + urlencode(query, doseq=True)

    # Split out classes from attributes
    # As we need to handle them specially
    extra_classes = None

    if "class" in attributes:
        extra_classes = attributes["class"]
        del attributes["class"]


    return template.render(
        path=path,
        alt=alt,
        width=int(width),
        height=int(height),
        extra_classes=extra_classes,
        attributes=attributes,
    )


sys.modules[__name__] = image_template
