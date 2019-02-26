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
   assets.ubuntu.com (e.g. ``/v1/9f6916dd-k8s-prometheus-light.png``)
-  ``alt`` (mandatory string): Alt text to describe the image
-  ``width`` (mandatory integer): The number of pixels wide the image
   should be
-  ``height`` (mandatory integer): The number of pixels high the image
   should be
-  ``col`` (optional): The number of Vanilla columns the image should
   span (helps define break points efficiently)

Usage
-----

The `image_template` function can be used directly to generate image Markup.

```
from canonicalwebteam import image_template

image_markup = image_template(
    path="/v1/9f6916dd-k8s-prometheus-light.png",
    alt="Operational dashboard",
    width="1040",
    height="585"
)
```

However, the most common usage is to add it to Django or Flask template contexts, as an `image` function.

Add lazysizes
~~~~~~~~~~~~~

The markup generated will use [lazysizes](https://github.com/aFarkas/lazysizes) format - it will use `data-src` instead of `src` and add the `lazyload` class.

Therefore to use this plugin you need to have lazysizes loaded on your pages. The simplest way to achieve this is to include this in your `<head>`:

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

    {% image path="/v1/9f6916dd-k8s-prometheus-light.png" alt="Operational dashboard" width="1040" height="585" %}

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
        path="/v1/9f6916dd-k8s-prometheus-light.png",
        alt="Operational dashboard",
        width="1040",
        height="585"
      ) | safe
    }}

Generated markup
~~~~~~~~~~~~~~~~

All the above examples will generate the following markup:

.. code:: html

    <img 
      data-srcset="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,w_412/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585 460w
                  ,https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,w_572/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585 620w
                  ,https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,w_720/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585 767w
                  ,https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto,w_990/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585 1030w"
      data-src="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585" 
      sizes="100vw"
      alt="test"
      width="1040"
      height="585"
      class="lazyload"
    />
    
    <noscript>
      <img
        src="https://res.cloudinary.com/canonical/image/fetch/q_auto,f_auto/https://assets.ubuntu.com/v1/9f6916dd-k8s-prometheus-light.png?w=1040&h=585"
        alt="Operational dashboard"
        width="1040"
        height="585"
      />
    </noscript>
