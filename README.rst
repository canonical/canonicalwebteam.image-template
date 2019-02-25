canonicalwebteam.image\_template
================================

A module to generate performant HTML image markup for images hosted on
``assets.ubuntu.com``. The markup will:

-  Use ``data-src`` attributes for
   `lazysizes <https://github.com/aFarkas/lazysizes>`__
-  Use predefined ``srcset`` break points
-  Resize the image with ``?w=XX&h=XX`` query parameters
-  Prefix all image URLs with cloudinary proxy URLs, for CDN and image
   transformations

Parameters
----------

-  ``path`` (mandatory string): The path to an asset on
   assets.ubuntu.com (e.g. ``/v1/9f61b97f-logo-ubuntu.svg``)
-  ``alt`` (mandatory string): Alt text to describe the image
-  ``width`` (mandatory integer): The number of pixels wide the image
   should be
-  ``height`` (mandatory integer): The number of pixels high the image
   should be
-  ``col`` (optional): The number of Vanilla columns the image should
   span (helps define break points efficiently)

Django usage
------------

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

Flask usage
-----------

.. code:: python3

    # app.py

    from canonicalwebteam import image_template
    from flask import Flask

    app = Flask(__name__)

    @app.context_processor
    def utility_processor():
        return {"image": image_template}
