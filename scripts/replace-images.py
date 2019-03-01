#! /usr/bin/env python3

# Standard library
import re
from io import BytesIO
from glob import glob
from PIL import Image
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from xml.etree import ElementTree

# Packages
from bs4 import BeautifulSoup


def get_properties(img_tag):
    img = BeautifulSoup(img_tag, "html.parser").find("img")
    width = None
    height = None

    if "width" in img.attrs:
        width = round(float(img.attrs["width"].rstrip("px")))
    if "height" in img.attrs:
        height = round(float(img.attrs["height"].rstrip("px")))

    if "class" in img.attrs and "p-inline-images__logo" in img.attrs["class"]:
        return False

    url = img.attrs["src"]
    alt = img.attrs["alt"]
    url_parts = urlparse(url)

    if "data:image" in url:
        return False

    if url_parts.netloc == "assets.ubuntu.com":
        # Use the assets server to resize the image
        # so we aren't caching more than we need in cloudinary

        params = parse_qs(url_parts.query)

        if "w" in params:
            width = int(params["w"][0])

        if "h" in params:
            width = int(params["h"][0])

    if not (width and height):
        # Download image
        image_file = BytesIO(urlopen(url).read())

        if url_parts.path[-4:] == ".svg":
            tree = ElementTree.fromstring(image_file.read().decode("utf-8"))

            if "width" in tree.attrib:
                real_width = round(float(tree.attrib["width"].rstrip("px")))
            else:
                if "viewBox" in tree.attrib:
                    matches = re.match(
                        "0 0 ([\d.]+) ([\d.]+)", tree.attrib["viewBox"]
                    )
                    real_width = round(float(matches.groups()[0]))

            if "height" in tree.attrib:
                real_height = round(float(tree.attrib["height"].rstrip("px")))
            else:
                if "viewBox" in tree.attrib:
                    matches = re.match(
                        "0 0 ([\d.]+) ([\d.]+)", tree.attrib["viewBox"]
                    )
                    real_height = round(float(matches.groups()[1]))

        else:
            image = Image.open(image_file)
            real_width, real_height = image.size

        if width and real_width > width and real_width <= 1040:
            # If we have width, calculate the relative height
            ratio = width / real_width
            height = round(real_height * ratio)
        elif height and real_height > height:
            # If we have height, calculate the relative width
            ratio = height / real_height
            width = round(real_width * ratio)
        else:
            width = real_width
            height = real_height

        if width > 1040:
            # Images never wider than 1040px
            width = 1040
            ratio = width / real_width
            height = round(real_height * ratio)

    del img.attrs["src"]
    del img.attrs["alt"]
    if "width" in img.attrs:
        del img.attrs["width"]
    if "height" in img.attrs:
        del img.attrs["height"]
    if "class" in img.attrs:
        img.attrs["class"] = " ".join(img.attrs["class"])

    return (url, alt, width, height, img.attrs)


for template_path in glob("**/*.html", recursive=True):
    with open(template_path) as template_file:
        template_content = template_file.read()

    img_tags = re.findall("<img[^>]+>", template_content)

    for img_tag in img_tags:
        try:
            img_properties = get_properties(img_tag)

            if not img_properties or img_properties[2] < 10:
                continue

            (url, alt, width, height, attrs) = img_properties

        except Exception as error:
            print(f"File: {template_path}")
            print(f"Image tag: {img_tag}")
            import ipdb

            ipdb.set_trace()
            raise error

        # print(image_template(**img_properties))
        attributes = ""
        for attr_name, attr_value in attrs.items():
            attributes += f' {attr_name}="{attr_value}"'

        template_content = re.sub(
            re.escape(img_tag),
            (
                "{% image "
                f'url="{url}" alt="{alt}" width="{width}" height="{height}"'
                f"{attributes}"
                " %}"
            ),
            template_content,
        )

    with open(template_path, "w") as template_file:
        template_file.write(template_content)
