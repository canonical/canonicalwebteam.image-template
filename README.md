# canonicalwebteam.image-template

[![PyPI](https://img.shields.io/pypi/v/canonicalwebteam.image-template)](https://pypi.org/project/canonicalwebteam.image-template/)
[![Tests](https://github.com/canonical-web-and-design/canonicalwebteam.image-template/workflows/Tests/badge.svg)](https://github.com/canonical-web-and-design/canonicalwebteam.image-template/actions?query=workflow%3ATests)
[![Code coverage](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.image-template/branch/main/graph/badge.svg)](https://codecov.io/gh/canonical-web-and-design/canonicalwebteam.image-template)

A module to generate performant HTML image markup for images. The markup
will:

- Use [native lazyloading](https://addyosmani.com/blog/lazy-loading/)
- Explicitly define `width` and `height` attributes to avoid the page jumping effect
- Prefix all image URLs with cloudinary CDN proxy URLs, to transform the image to the optimal size
- Use predefined (2x) `srcset` break points for hidef screens

## Parameters

- `url` (mandatory string): The url to an image (e.g. `https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png`)
- `alt` (mandatory string): Alt text to describe the image
- `hi_def` (mandatory boolean): Has an image been uploaded 2x the width and height of the desired size
- `width` (mandatory integer): The number of pixels wide the image should be
- `height` (optional integer): The number of pixels high the image should be
- `fill` (optional boolean): Set the crop mode to ["fill"](https://cloudinary.com/documentation/image_transformation_reference#crop_parameter)
- `loading` (optional string, default: "lazy"): Set to ["auto" or "eager"](https://addyosmani.com/blog/lazy-loading/) to disable lazyloading
- `attrs` (optional dictionary): Extra `<img>` attributes (e.g. `class` or `id`) can be passed as additional arguments

## Usage

### Local development

For local development, it's best to test this module with one of our website projects like [ubuntu.com](https://github.com/canonical-web-and-design/ubuntu.com/). For more information, follow [this guide (internal only)](https://discourse.canonical.com/t/how-to-run-our-python-modules-for-local-development/308).

### Application code

The `image_template` function can be used directly to generate image Markup.

``` python3
from canonicalwebteam import image_template

image_markup = image_template(
    url="https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg",
    alt="",
    width="534",
    height="319",
    hi_def=True,
    loading="auto",
	fill=True,
    attrs={"class": "hero", "id": "openstack-hero"},
)
```

However, the most common usage is to add it to Django or Flask template contexts, as an `image` function.

### Django usage

Add it as a template tag:

``` python3
# myapp/templatetags.py

from canonicalwebteam import image_template
from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.simple_tag
def image(*args, **kwargs):
    return mark_safe(image_template(*args, **kwargs))


# settings.py

TEMPLATES[0]["OPTIONS"]["builtins"].append("myapp.templatetags")
```

Use it in templates:

``` html
# templates/mytemplate.html

{% image url="https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png" alt="Operational dashboard" width="1040" height="585" hi_def=True fill=True %}
```

### Flask usage

Add it as a template tag:

``` python3
# app.py

from canonicalwebteam import image_template
from flask import Flask

app = Flask(__name__)

@app.context_processor
def utility_processor():
    return {"image": image_template}
```

Use it in templates, e.g.::

``` html
# templates/mytemplate.html

{{
  image(
    url="https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg",
    alt="",
    width="534",
    height="319",
    hi_def=True,
	fill=True,
    loading="auto",
    attrs={"class": "hero", "id": "openstack-hero"},
  ) | safe
}}
```

## Generated markup

The output image markup will be e.g.:

``` html
<img
    src="https://res.cloudinary.com/canonical/image/fetch/f_auto,q_auto,fl_sanitize,w_534,h_319,c_fill/https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg"
    srcset="https://res.cloudinary.com/canonical/image/fetch/f_auto,q_auto,fl_sanitize,w_1068,h_638,c_fill/https://assets.ubuntu.com/v1/450d7c2f-openstack-hero.svg 2x"
    alt=""
    width="534"
    height="319"
    loading="auto"
    class="hero"
    id="openstack hero"
/>
```

## VS Code Snippet

To add the required markup for this template as a User Snippet, add the following as a HTML snippet (User Snippets under File > Preferences, or Code > Preferences on macOS):

```
"Image module": {
	"prefix": "image-module",
	"body": [
		"{{",
		"	image_template(",
		"		url=\"$1\",",
		"		alt=\"$2\",",
		"		height=\"$3\",",
		"		width=\"$4\",",
		"		hi_def=$5True,",
		"		loading=\"auto|lazy$6\",",
		"		attrs={\"class\": \"$7\"}",
		"	) | safe",
		"}}"
	],
	"description": "Image module include"
}"
```
