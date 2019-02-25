# Standard library
import os
import sys
from urllib.parse import urlparse, parse_qs, urlencode

# Packages
from jinja2 import Environment, FileSystemLoader


parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(path, alt, width, height):
    """
    Generate image markup
    """

    parse_result = urlparse(path)

    if parse_result.netloc:
        raise Exception("path should not contain a hostname")

    query = parse_qs(parse_result.query)
    query['w'] = int(width)
    query['h'] = int(height)

    path = path.lstrip('/') + '?' + urlencode(query, doseq=True)

    return template.render(path=path, alt=alt, width=width, height=height)


sys.modules[__name__] = image_template
