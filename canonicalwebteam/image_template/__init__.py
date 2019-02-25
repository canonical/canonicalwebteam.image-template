# Standard library
import os
import sys

# Packages
from jinja2 import Environment, FileSystemLoader


parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")


def image_template(url, alt, width, height):
    """
    Generate image markup
    """

    return template.render(url=url, alt=alt, width=width, height=height)


sys.modules[__name__] = image_template
