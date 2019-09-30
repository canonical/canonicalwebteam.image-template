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
-  ``lazy`` (optional boolean): Defaults to True, set to False to receive the benefits of srcset without lazysizes

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

    <script src="https://assets.ubuntu.com/v1/842d27d3-lazysizes.min.js" async></script>

NOTE: When JS is disabled Chrome will display a broken image and alt text for the lazysizes version which can cause layout issues.
It's advisable to add the CSS below to the sites CSS.

.. code:: css

   .lazyload {
      visibility: hidden;
      height: 0;
      width: 0;
      margin: 0;
      padding: 0;
   }

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
        hi_def=True,
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

