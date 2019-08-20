canonicalwebteam.image\_template
================================

A module to generate performant HTML image markup for images. The markup
will:

-  Use ``data-src`` attributes for
   `lazysizes <https://github.com/aFarkas/lazysizes>`__
-  Use predefined ``srcset`` break points
-  Resize ``assets.ubuntu.com`` images with ``?w=XX&h=XX`` query
   parameters
-  Prefix all image URLs with cloudinary proxy URLs, for CDN and image
   transformations

Parameters
----------

-  ``url`` (mandatory string): The url to an image (e.g.
   ``https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png``)
-  ``alt`` (mandatory string): Alt text to describe the image
-  ``width`` (mandatory integer): The number of pixels wide the image
   should be
-  ``height`` (mandatory integer): The number of pixels high the image
   should be
-  ``hi_def`` (mandatory boolean): Has an image been uploaded 2x the width and height of the desired size
-  ``extra_classes`` (optional): Class string to add to img element
-  `extra attributes` (optional): Extra ``<img>`` attributes (e.g. 
   ``id``) can be passed as additional arguments

Usage
-----

The ``image_template`` function can be used directly to generate image
Markup.

.. code:: python3

    from canonicalwebteam import image_template

    image_markup = image_template(
        url="https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png",
        alt="Operational dashboard",
        width="1040",
        height="585",
        hi_def=True
    )

However, the most common usage is to add it to Django or Flask template
contexts, as an ``image`` function.

Add lazysizes
~~~~~~~~~~~~~

The markup generated will use
`lazysizes <https://github.com/aFarkas/lazysizes>`__ format - it will
use data-src instead of src and add the lazyload class.

Therefore to use this plugin you need to have lazysizes loaded on your
pages. The simplest way to achieve this is to include this in your
``<head>``:

.. code:: html

    <script src="https://assets.ubuntu.com/v1/842d27d3-lazysizes.min.js" async=""></script>

Django usage
~~~~~~~~~~~~

Add it as a template tag:

.. code:: python3

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

Use it in templates:

.. code:: html

    # templates/mytemplate.html

    {% image url="https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png" alt="Operational dashboard" width="1040" height="585" hi_def=True %}

Flask usage
~~~~~~~~~~~

Add it as a template tag:

.. code:: python3

    # app.py

    from canonicalwebteam import image_template
    from flask import Flask

    app = Flask(__name__)

    @app.context_processor
    def utility_processor():
        return {"image": image_template}

Use it in templates:

.. code:: html

    # templates/mytemplate.html

    {{
      image(
        url="https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png",
        alt="Operational dashboard",
        width="1040",
        height="585",
        hi_def: True,
      ) | safe
    }}

Generated markup
~~~~~~~~~~~~~~~~

All the above examples will generate the following markup:

.. code:: html

    <img 
      data-srcset="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_2080,h_1170/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png x2"
      data-src="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_1040,h_585/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png" 
      alt="Operational dashboard"
      width="1040"
      height="585"
      class="lazyload"
    />

    <noscript>
      <img
        srcset="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_2080,h_1170/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png x2"
        src="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_1040,h_585/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png" 
        alt="Operational dashboard"
        width="1040"
        height="585"
      />
    </noscript>


File sizes
~~~~~~~~~~

Source:
https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png
2560 x 1440 - 300.62kb

Asset server x2 resize:
https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=2080&h=1170
2080 x 1170 - 595.67kb

Asset server resize:
https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585
1040 x 585 - 221.21kb

Asset server resize x2 + Cloudinary x2 resize:
https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png%3Fw%3D2080%26h%3D1170
2080 x 1170 - 194.97kb

Asset server resize x1 + Cloudinary x1 resize:
https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize/https%3A//assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png%3Fw%3D1040%26h%3D585
1040 x 585 - 109.38kb

Cloudinary x2 resize:
https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_2080,h_1170/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png
2080 x 1170 - 163.38

Cloudinary x1 resize:
https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,fl_sanitize,w_1040,h_585/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png
1040 x 585 - 62.80kb
