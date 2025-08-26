# JavaScript Image Template Implementation

This is a JavaScript port of the Python `image_template` function that generates responsive image markup with optimized srcset and sizes attributes.

## Features

- 🚀 **Cloudinary Integration**: Automatic image optimization through Cloudinary
- 🎯 **Smart Format Detection**: Bypasses processing for already-optimized formats (SVG, WebP, AVIF, GIF)
- 📱 **Responsive Images**: Generates srcset for multiple screen sizes
- 🌐 **Universal Compatibility**: Works in both browser and Node.js environments
- ⚡ **Performance Optimized**: Only generates srcset for images larger than 100px
- 🎨 **Flexible Output**: Supports both HTML string and attributes object output

## Installation

Simply include the `image_template.js` file in your project:

### Browser
```html
<script src="image_template.js"></script>
```

### Node.js
```javascript
const { ImageTemplate, imageTemplate } = require('./image_template.js');
```

### ES Modules
```javascript
import { ImageTemplate, imageTemplate } from './image_template.js';
```

## Usage

### Basic Usage

```javascript
// Simple image with Cloudinary optimization
const html = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Description of image',
  width: 800,
  height: 600
});

console.log(html);
// Output: <img src="https://res.cloudinary.com/canonical/image/fetch/f_auto,q_auto,fl_sanitize,w_800/https%3A%2F%2Fexample.com%2Fimage.jpg" srcset="..." sizes="..." alt="Description of image" width="800" height="600" loading="lazy" />
```

### SVG and Optimized Formats (Bypass Cloudinary)

```javascript
// SVG files bypass Cloudinary processing
const svgHtml = imageTemplate({
  url: 'https://example.com/logo.svg',
  alt: 'Company logo',
  width: 200,
  height: 100
});

console.log(svgHtml);
// Output: <img src="https://example.com/logo.svg" alt="Company logo" width="200" height="100" loading="lazy" />
```

### Advanced Options

```javascript
const advancedHtml = imageTemplate({
  url: 'https://example.com/hero.png',
  alt: 'Hero image',
  width: 1200,
  height: 800,
  fill: true,                    // Crop and fill to exact dimensions
  eSharpen: true,               // Apply sharpening
  fmt: 'webp',                  // Force WebP format
  loading: 'eager',             // Load immediately
  hiDef: true,                  // Enable high-DPI support (up to 2x)
  attrs: {                      // Additional HTML attributes
    'class': 'hero-image',
    'data-testid': 'main-hero'
  },
  srcsetWidths: [400, 800, 1200, 1600], // Custom srcset widths
  sizes: '(min-width: 1200px) 1200px, 100vw' // Custom sizes attribute
});
```

### Attributes Mode

```javascript
// Get attributes object instead of HTML string
const attrs = imageTemplate({
  url: 'https://example.com/thumbnail.jpg',
  alt: 'Thumbnail',
  width: 150,
  height: 150,
  outputMode: 'attrs'
});

console.log(attrs);
// Output: {
//   src: 'https://res.cloudinary.com/canonical/image/fetch/...',
//   srcset: '...',
//   sizes: '...',
//   alt: 'Thumbnail',
//   width: 150,
//   height: 150,
//   loading: 'lazy'
// }
```

## API Reference

### `imageTemplate(options)`

Generates responsive image markup with optimized srcset and sizes.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `url` | string | **required** | Image URL |
| `alt` | string | **required** | Alt text for accessibility |
| `width` | number | **required** | Primary image width |
| `height` | number | `null` | Image height (optional) |
| `fill` | boolean | `false` | Whether to crop and fill to exact dimensions |
| `eSharpen` | boolean | `false` | Whether to apply sharpening |
| `loading` | string | `'lazy'` | Loading strategy (`'lazy'`, `'eager'`, `'auto'`) |
| `fmt` | string | `'auto'` | Image format (`'auto'`, `'webp'`, `'jpg'`, etc.) |
| `attrs` | object | `{}` | Additional HTML attributes |
| `outputMode` | string | `'html'` | Output mode (`'html'` or `'attrs'`) |
| `sizes` | string | `'(min-width: {}px) {}px, 100vw'` | Responsive sizes attribute template |
| `srcsetWidths` | number[] | `[460, 620, 1036, 1681]` | Custom widths for srcset generation |
| `hiDef` | boolean | `false` | Enable high-DPI support (up to 2x) |

#### Returns

- **HTML mode**: Returns an HTML string with the `<img>` tag
- **Attrs mode**: Returns an object with image attributes

## Format Bypass Logic

Certain image formats bypass Cloudinary processing to preserve their characteristics:

- **SVG** (`.svg`): Vector format that becomes blurry when converted to raster
- **WebP** (`.webp`): Already optimized modern format
- **AVIF** (`.avif`): Already optimized modern format
- **GIF** (`.gif`): Animation would be lost in conversion

These formats return the original URL directly without srcset generation.

## Cloudinary Optimizations

For supported formats (JPG, PNG, etc.), the following Cloudinary optimizations are applied:

- `f_auto` or custom format: Automatic format selection or specified format
- `q_auto`: Automatic quality optimization
- `fl_sanitize`: Sanitize SVG content for security
- `e_sharpen`: Apply sharpening (when enabled)
- `c_fill`: Crop and fill to exact dimensions (when enabled)
- `w_*`: Width transformations for responsive images

## Responsive Images

The implementation generates srcset attributes for images larger than 100px using these default breakpoints:

- 460px (small mobile)
- 620px (large mobile)
- 1036px (tablet)
- 1681px (desktop)

You can customize these widths using the `srcsetWidths` parameter.

## Testing

### Browser Testing

Open `test_js_implementation.html` in your browser to see visual tests of the implementation.

### Node.js Testing

```bash
node test_js_node.js
```

This will run comprehensive tests covering:
- Regular image processing with Cloudinary
- Format bypass logic for SVG, WebP, AVIF, and GIF
- Custom attributes and options
- Error handling
- Both HTML and attributes output modes

## Browser Compatibility

- **Modern Browsers**: Full support (Chrome 60+, Firefox 55+, Safari 12+, Edge 79+)
- **Legacy Browsers**: Basic functionality (may need URL polyfill for older browsers)

## Node.js Compatibility

- **Node.js 12+**: Full support
- **Older versions**: May need URL polyfill

## Error Handling

The implementation includes proper error handling for:

- Invalid URLs (missing hostname)
- Invalid output modes
- Malformed parameters

Errors are thrown as standard JavaScript `Error` objects with descriptive messages.

## Performance Considerations

- **Srcset Generation**: Only generated for images > 100px width
- **High-DPI Support**: Capped at 2x to avoid excessive payload
- **URL Encoding**: Proper encoding/decoding to prevent double-encoding issues
- **Memory Efficient**: No unnecessary object creation or string manipulation

## Differences from Python Implementation

The JavaScript implementation maintains feature parity with the Python version:

- ✅ Same API and parameter names
- ✅ Identical Cloudinary URL generation
- ✅ Same format bypass logic
- ✅ Equivalent HTML output
- ✅ Same error handling behavior
- ✅ Compatible srcset generation logic

The only differences are environment-specific (e.g., HTML escaping implementation).