/**
 * JavaScript implementation of the Python image_template function
 * Generates responsive image markup with optimized srcset and sizes
 */

class ImageTemplate {
  constructor() {
    this.cloudinaryUrlBase = 'https://res.cloudinary.com/canonical/image/fetch';
    this.bypassExtensions = ['.svg', '.webp', '.avif', '.gif'];
  }

  /**
   * Generate responsive image markup with optimized srcset and sizes
   * 
   * @param {Object} options - Configuration options
   * @param {string} options.url - Image URL
   * @param {string} options.alt - Alt text for accessibility
   * @param {number} options.width - Primary image width
   * @param {number} [options.height] - Image height (optional)
   * @param {boolean} [options.fill=false] - Whether to crop and fill to exact dimensions
   * @param {boolean} [options.eSharpen=false] - Whether to apply sharpening
   * @param {string} [options.loading='lazy'] - Loading strategy ('lazy', 'auto')
   * @param {string} [options.fmt='auto'] - Image format ('auto', 'webp', 'jpg', etc.)
   * @param {Object} [options.attrs={}] - Additional HTML attributes
   * @param {string} [options.outputMode='html'] - 'html' or 'attrs'
   * @param {string} [options.sizes='(min-width: {}px) {}px, 100vw'] - Responsive sizes attribute template
   * @param {number[]} [options.srcsetWidths] - Custom widths for srcset generation
   * @param {boolean} [options.hiDef=false] - Enable high-DPI support (up to 2x)
   * @returns {string|Object} HTML string or attributes object
   */
  imageTemplate({
    url,
    alt,
    width,
    height = null,
    fill = false,
    eSharpen = false,
    loading = 'lazy',
    fmt = 'auto',
    attrs = {},
    outputMode = 'html',
    sizes = '(min-width: {}px) {}px, 100vw',
    srcsetWidths = null,
    hiDef = false
  }) {
    const urlParts = new URL(url);

    // Check if the image is a format that doesn't need Cloudinary optimization
    // SVG: Vector format, converting to WebP makes it blurry
    // WebP/AVIF: Already optimized modern formats
    // GIF: Animation would be lost in conversion
    const shouldBypass = this.bypassExtensions.some(ext => 
      urlParts.pathname.toLowerCase().endsWith(ext)
    );

    if (shouldBypass) {
      const imageAttrs = {
        src: url,
        alt: alt,
        width: parseInt(width),
        height: height,
        loading: loading,
        attrs: attrs
      };

      if (outputMode === 'html') {
        return this.renderHtml(imageAttrs);
      } else if (outputMode === 'attrs') {
        const mergedAttrs = { ...imageAttrs, ...attrs };
        delete mergedAttrs.attrs;
        return mergedAttrs;
      } else {
        throw new Error("outputMode must be 'html' or 'attrs'");
      }
    }

    // Default cloudinary optimizations
    // https://cloudinary.com/documentation/image_transformations
    const cloudinaryOptions = [
      `f_${fmt}`,
      'q_auto',  // Auto optimize quality
      'fl_sanitize'  // Sanitize SVG content
    ];

    if (eSharpen) {
      cloudinaryOptions.push('e_sharpen');
    }

    // If the original image does not match the requested
    // ratio set crop and fill see
    // https://cloudinary.com/documentation/image_transformation_reference#crop_parameter
    if (fill) {
      cloudinaryOptions.push('c_fill');
    }

    if (!urlParts.hostname) {
      throw new Error('url must contain a hostname');
    }

    const stdDefCloudinaryOptions = [...cloudinaryOptions];
    stdDefCloudinaryOptions.push(`w_${width}`);
    const stdDefCloudinaryAttrs = stdDefCloudinaryOptions.join(',');

    // Encode the URL properly
    const encodedUrl = encodeURIComponent(decodeURIComponent(url));
    const imageSrc = `${this.cloudinaryUrlBase}/${stdDefCloudinaryAttrs}/${encodedUrl}`;

    // Generate srcset values with optimized logic for real-world usage
    // https://vanillaframework.io/docs/settings/breakpoint-settings
    if (srcsetWidths === null) {
      srcsetWidths = [460, 620, 1036, 1681];
    }

    const widthInt = parseInt(width);
    const srcset = [];

    // Only generate srcset for images larger than 100px to avoid
    // unnecessary overhead
    if (widthInt > 100) {
      const maxSrcsetWidth = Math.max(...srcsetWidths);
      // When hiDef is enabled, allow slightly larger for high-DPI
      // But cap at 2x to avoid excessive payload
      const maxWidthLimit = hiDef 
        ? Math.min(widthInt * 2, maxSrcsetWidth)
        : Math.min(widthInt, maxSrcsetWidth);

      const createSrcsetUrl = (width, options) => {
        const widthOptions = [...options];
        widthOptions.push(`w_${width}`);
        const widthAttrs = widthOptions.join(',');
        return `${this.cloudinaryUrlBase}/${widthAttrs}/${encodedUrl} ${width}w`;
      };

      // Generate srcset entries for standard widths
      const filteredWidths = srcsetWidths.filter(w => w <= maxWidthLimit);
      srcset.push(...filteredWidths.map(w => createSrcsetUrl(w, cloudinaryOptions)));

      // Add original width if needed
      const existingWidths = new Set(filteredWidths);
      if (widthInt <= maxWidthLimit && !existingWidths.has(widthInt)) {
        srcset.push(createSrcsetUrl(widthInt, cloudinaryOptions));
      }
    }

    const imageSrcset = srcset.join(', ');

    // Format sizes string
    let formattedSizes = sizes;
    try {
      formattedSizes = sizes.replace(/\{\}/g, width);
    } catch (e) {
      // Keep original sizes if formatting fails
    }

    const imageAttrs = {
      src: imageSrc,
      srcset: imageSrcset,
      sizes: formattedSizes,
      alt: alt,
      width: parseInt(width),
      height: height,
      loading: loading,
      attrs: attrs
    };

    if (!imageSrcset) {
      delete imageAttrs.srcset;
      delete imageAttrs.sizes;
    }

    if (outputMode === 'html') {
      return this.renderHtml(imageAttrs);
    } else if (outputMode === 'attrs') {
      const mergedAttrs = { ...imageAttrs, ...attrs };
      delete mergedAttrs.attrs;
      return mergedAttrs;
    } else {
      throw new Error("outputMode must be 'html' or 'attrs'");
    }
  }

  /**
   * Render HTML string from image attributes
   * @param {Object} imageAttrs - Image attributes object
   * @returns {string} HTML string
   */
  renderHtml(imageAttrs) {
    let html = '<img';
    
    // Add src attribute
    html += ` src="${this.escapeHtml(imageAttrs.src)}"`;
    
    // Add srcset if present
    if (imageAttrs.srcset) {
      html += ` srcset="${this.escapeHtml(imageAttrs.srcset)}"`;
    }
    
    // Add sizes if present
    if (imageAttrs.sizes) {
      html += ` sizes="${this.escapeHtml(imageAttrs.sizes)}"`;
    }
    
    // Add alt attribute
    html += ` alt="${this.escapeHtml(imageAttrs.alt)}"`;
    
    // Add width attribute
    html += ` width="${imageAttrs.width}"`;
    
    // Add height if present
    if (imageAttrs.height !== null && imageAttrs.height !== undefined) {
      html += ` height="${imageAttrs.height}"`;
    }
    
    // Add loading attribute
    html += ` loading="${this.escapeHtml(imageAttrs.loading)}"`;
    
    // Add additional attributes
    if (imageAttrs.attrs && typeof imageAttrs.attrs === 'object') {
      for (const [attrName, attrValue] of Object.entries(imageAttrs.attrs)) {
        html += ` ${attrName}="${this.escapeHtml(String(attrValue))}"`;
      }
    }
    
    html += ' />';
    return html;
  }

  /**
   * Escape HTML special characters
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   */
  escapeHtml(text) {
    if (typeof document !== 'undefined') {
      // Browser environment
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    } else {
      // Node.js environment - manual escaping
      return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }
  }
}

// Create a singleton instance for easy usage
const imageTemplateInstance = new ImageTemplate();

/**
 * Convenience function that matches the Python API
 * @param {Object} options - Same options as ImageTemplate.imageTemplate
 * @returns {string|Object} HTML string or attributes object
 */
function imageTemplate(options) {
  return imageTemplateInstance.imageTemplate(options);
}

// Export for different module systems
if (typeof module !== 'undefined' && module.exports) {
  // Node.js
  module.exports = { ImageTemplate, imageTemplate };
} else if (typeof define === 'function' && define.amd) {
  // AMD
  define([], function() {
    return { ImageTemplate, imageTemplate };
  });
} else {
  // Browser global
  window.ImageTemplate = ImageTemplate;
  window.imageTemplate = imageTemplate;
}