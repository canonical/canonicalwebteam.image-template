# Standard library
import os
import sys
from urllib.parse import quote, unquote, urlparse

# Packages
from jinja2 import Environment, FileSystemLoader

parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = Environment(loader=FileSystemLoader(parent_dir + "/templates"))
template = env.get_template("image_template.html")
cloudinary_url_base = "https://res.cloudinary.com/canonical/image/fetch"


def image_template(
    url,
    alt,
    width,
    height=None,
    fill=False,
    e_sharpen=False,
    loading="lazy",
    fmt="auto",
    attrs={},
    output_mode="html",
    sizes="(min-width: {}px) {}px, 100vw",
    srcset_widths=None,
    hi_def=False,
):
    """
    Generate responsive image markup with optimized srcset and sizes.
    
    Args:
        url: Image URL
        alt: Alt text for accessibility
        width: Primary image width
        height: Image height (optional)
        fill: Whether to crop and fill to exact dimensions
        e_sharpen: Whether to apply sharpening
        loading: Loading strategy ('lazy', 'eager', 'auto')
        fmt: Image format ('auto', 'webp', 'jpg', etc.)
        attrs: Additional HTML attributes
        output_mode: 'html' or 'attrs'
        sizes: Responsive sizes attribute template
        srcset_widths: Custom widths for srcset generation
        hi_def: Enable conservative high-DPI support (up to 1.25x, capped at 1600px)
    """

    url_parts = urlparse(url)

    # Default cloudinary optimisations
    # https://cloudinary.com/documentation/image_transformations
    cloudinary_options = [
        "f_" + str(fmt),
        "q_auto",  # Auto optimise quality
        "fl_sanitize",  # Sanitize SVG content
    ]

    if e_sharpen:
        cloudinary_options.append("e_sharpen")

    # If the original image does not match the requested
    # ratio set crop and fill see
    # https://cloudinary.com/documentation/image_transformation_reference#crop_parameter
    if fill:
        cloudinary_options.append("c_fill")

    if not url_parts.netloc:
        raise Exception("url must contain a hostname")

    std_def_cloudinary_options = cloudinary_options.copy()
    std_def_cloudinary_options.append("w_" + str(width))
    std_def_cloudinary_attrs = ",".join(std_def_cloudinary_options)
    image_src = f"{cloudinary_url_base}/{std_def_cloudinary_attrs}/{url}"

    # Generate srcset values with optimized logic for real-world usage
    # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img#attr-srcset
    # Optimized for container max-width of 1386px on 2560px displays
    # Most images are 50% or 100% of container, so max effective size is ~1386px
    # Conservative approach to minimize payload while maintaining quality
    if srcset_widths is None:
        # Focused on actual breakpoints: mobile, tablet, desktop
        # Removed unnecessary large sizes that increase payload
        srcset_widths = [320, 480, 768, 1024]
    
    width_int = int(width)
    srcset = []
    
    # Only generate srcset for images larger than 100px to avoid unnecessary overhead
    if width_int > 100:
        # Conservative approach: limit srcset to practical sizes
        # For most use cases, going beyond 1386px is unnecessary
        max_practical_width = min(width_int, 1386)
        
        # When hi_def is enabled, allow slightly larger for high-DPI
        # But cap at 1.25x to avoid excessive payload
        if hi_def:
            max_width_limit = min(width_int * 1.25, 1600)  # Conservative 1.25x, capped at 1600px
        else:
            max_width_limit = max_practical_width
        
        # Include widths that make sense for responsive design
        for srcset_width in srcset_widths:
            if srcset_width <= max_width_limit:
                srcset_options = cloudinary_options.copy()
                srcset_options.append("w_" + str(srcset_width))
                srcset_attrs = ",".join(srcset_options)
                srcset.append(
                    f"{cloudinary_url_base}/{srcset_attrs}/{url} {srcset_width}w"
                )
        
        # Include the original width only if it's within practical limits
        # and not already present in srcset
        if (width_int <= max_width_limit and 
            width_int not in [int(w) for w in srcset_widths if w <= max_width_limit]):
            srcset_options = cloudinary_options.copy()
            srcset_options.append("w_" + str(width_int))
            srcset_attrs = ",".join(srcset_options)
            srcset.append(
                f"{cloudinary_url_base}/{srcset_attrs}/{url} {width_int}w"
            )

    image_srcset = ", ".join(srcset)

    try:
        sizes_attr = sizes.format(width, width)
    except (IndexError, KeyError):
        sizes_attr = sizes

    image_attrs = {
        "src": image_src,
        "srcset": image_srcset,
        "sizes": sizes_attr,
        "alt": alt,
        "width": int(width),
        "height": height,
        "loading": loading,
        "attrs": attrs,
    }

    if not image_srcset:
        del image_attrs["srcset"]
        del image_attrs["sizes"]

    if output_mode == "html":
        return template.render(**image_attrs)
    elif output_mode == "attrs":
        merged_attrs = {**image_attrs, **attrs}
        del merged_attrs["attrs"]
        return merged_attrs
    else:
        raise ValueError("output_mode must be 'html' or 'attrs'")


sys.modules[__name__] = image_template
