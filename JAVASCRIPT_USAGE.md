# Using Image Template in JavaScript Projects

This guide shows how to integrate the JavaScript image template implementation into your JavaScript/TypeScript projects.

## Installation Options

### Option 1: NPM Package (Recommended)

```bash
# Install from npm (when published)
npm install @canonical/image-template

# Or with yarn
yarn add @canonical/image-template

# Or with pnpm
pnpm add @canonical/image-template
```

### Option 2: Direct File Include

Download the files directly from this repository:

```bash
# Copy the main files to your project
cp image_template.js your-project/src/utils/
cp image_template.d.ts your-project/src/utils/  # For TypeScript projects
```

### Option 3: CDN (Browser Only)

```html
<!-- Include from CDN (when available) -->
<script src="https://cdn.jsdelivr.net/npm/@canonical/image-template@latest/image_template.js"></script>
```

## Usage in Different JavaScript Environments

### Node.js (CommonJS)

```javascript
const { imageTemplate } = require('@canonical/image-template');

// Generate responsive image HTML
const html = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Product image',
  width: 800,
  height: 600
});

console.log(html);
```

### ES Modules (Modern JavaScript)

```javascript
import { imageTemplate } from '@canonical/image-template';

// Generate responsive image HTML
const html = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Product image',
  width: 800,
  height: 600
});

document.getElementById('container').innerHTML = html;
```

### TypeScript

```typescript
import { imageTemplate, ImageTemplateOptions } from '@canonical/image-template';

// Type-safe usage
const options: ImageTemplateOptions = {
  url: 'https://example.com/image.jpg',
  alt: 'Product image',
  width: 800,
  height: 600,
  fill: true,
  attrs: {
    class: 'product-image',
    'data-testid': 'main-product'
  }
};

const html: string = imageTemplate(options) as string;
```

### Browser (Global Script)

```html
<script src="path/to/image_template.js"></script>
<script>
  // Use global imageTemplate function
  const html = imageTemplate({
    url: 'https://example.com/image.jpg',
    alt: 'Product image',
    width: 800,
    height: 600
  });
  
  document.getElementById('container').innerHTML = html;
</script>
```

## Framework Integration Examples

### React

```jsx
import React from 'react';
import { imageTemplate } from '@canonical/image-template';

function ProductImage({ src, alt, width, height }) {
  const imageHtml = imageTemplate({
    url: src,
    alt,
    width,
    height,
    outputMode: 'attrs'
  });
  
  return (
    <img
      src={imageHtml.src}
      srcSet={imageHtml.srcset}
      sizes={imageHtml.sizes}
      alt={imageHtml.alt}
      width={imageHtml.width}
      height={imageHtml.height}
      loading={imageHtml.loading}
    />
  );
}

// Or using dangerouslySetInnerHTML (less safe)
function ProductImageHTML({ src, alt, width, height }) {
  const imageHtml = imageTemplate({
    url: src,
    alt,
    width,
    height
  });
  
  return <div dangerouslySetInnerHTML={{ __html: imageHtml }} />;
}
```

### Vue.js

```vue
<template>
  <div v-html="imageHtml"></div>
</template>

<script>
import { imageTemplate } from '@canonical/image-template';

export default {
  props: ['src', 'alt', 'width', 'height'],
  computed: {
    imageHtml() {
      return imageTemplate({
        url: this.src,
        alt: this.alt,
        width: this.width,
        height: this.height
      });
    }
  }
};
</script>
```

### Angular

```typescript
// image.component.ts
import { Component, Input } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { imageTemplate } from '@canonical/image-template';

@Component({
  selector: 'app-image',
  template: '<div [innerHTML]="safeHtml"></div>'
})
export class ImageComponent {
  @Input() src!: string;
  @Input() alt!: string;
  @Input() width!: number;
  @Input() height?: number;
  
  constructor(private sanitizer: DomSanitizer) {}
  
  get safeHtml(): SafeHtml {
    const html = imageTemplate({
      url: this.src,
      alt: this.alt,
      width: this.width,
      height: this.height
    });
    return this.sanitizer.bypassSecurityTrustHtml(html as string);
  }
}
```

### Svelte

```svelte
<script>
  import { imageTemplate } from '@canonical/image-template';
  
  export let src;
  export let alt;
  export let width;
  export let height;
  
  $: imageHtml = imageTemplate({
    url: src,
    alt,
    width,
    height
  });
</script>

{@html imageHtml}
```

## Build Tool Configuration

### Webpack

```javascript
// webpack.config.js
module.exports = {
  // ... other config
  resolve: {
    alias: {
      '@canonical/image-template': path.resolve(__dirname, 'node_modules/@canonical/image-template/image_template.js')
    }
  }
};
```

### Vite

```javascript
// vite.config.js
import { defineConfig } from 'vite';

export default defineConfig({
  // ... other config
  resolve: {
    alias: {
      '@canonical/image-template': path.resolve(__dirname, 'node_modules/@canonical/image-template/image_template.js')
    }
  }
});
```

### Rollup

```javascript
// rollup.config.js
import resolve from '@rollup/plugin-node-resolve';

export default {
  // ... other config
  plugins: [
    resolve({
      preferBuiltins: false
    })
  ]
};
```

## Server-Side Rendering (SSR)

### Next.js

```javascript
// pages/product/[id].js
import { imageTemplate } from '@canonical/image-template';

export async function getServerSideProps({ params }) {
  const product = await fetchProduct(params.id);
  
  // Generate image HTML on server
  const imageHtml = imageTemplate({
    url: product.imageUrl,
    alt: product.name,
    width: 800,
    height: 600
  });
  
  return {
    props: {
      product,
      imageHtml
    }
  };
}

export default function Product({ product, imageHtml }) {
  return (
    <div>
      <h1>{product.name}</h1>
      <div dangerouslySetInnerHTML={{ __html: imageHtml }} />
    </div>
  );
}
```

### Nuxt.js

```javascript
// plugins/image-template.js
import { imageTemplate } from '@canonical/image-template';

export default ({ app }, inject) => {
  inject('imageTemplate', imageTemplate);
};
```

```vue
<!-- pages/product/_id.vue -->
<template>
  <div>
    <h1>{{ product.name }}</h1>
    <div v-html="imageHtml"></div>
  </div>
</template>

<script>
export default {
  async asyncData({ params, $imageTemplate }) {
    const product = await fetchProduct(params.id);
    
    const imageHtml = $imageTemplate({
      url: product.imageUrl,
      alt: product.name,
      width: 800,
      height: 600
    });
    
    return {
      product,
      imageHtml
    };
  }
};
</script>
```

## Testing

### Jest

```javascript
// __tests__/image-template.test.js
const { imageTemplate } = require('@canonical/image-template');

describe('imageTemplate', () => {
  test('generates HTML for regular images', () => {
    const html = imageTemplate({
      url: 'https://example.com/test.jpg',
      alt: 'Test image',
      width: 400,
      height: 300
    });
    
    expect(html).toContain('src="https://res.cloudinary.com');
    expect(html).toContain('srcset=');
    expect(html).toContain('alt="Test image"');
  });
  
  test('bypasses Cloudinary for SVG', () => {
    const html = imageTemplate({
      url: 'https://example.com/logo.svg',
      alt: 'Logo',
      width: 200
    });
    
    expect(html).toContain('src="https://example.com/logo.svg"');
    expect(html).not.toContain('srcset=');
  });
});
```

## Performance Considerations

### Lazy Loading

```javascript
// Lazy load the image template function
const loadImageTemplate = async () => {
  const { imageTemplate } = await import('@canonical/image-template');
  return imageTemplate;
};

// Use when needed
loadImageTemplate().then(imageTemplate => {
  const html = imageTemplate({
    url: 'https://example.com/image.jpg',
    alt: 'Lazy loaded image',
    width: 800
  });
  document.getElementById('container').innerHTML = html;
});
```

### Caching

```javascript
// Simple memoization for repeated calls
const imageTemplateCache = new Map();

function cachedImageTemplate(options) {
  const key = JSON.stringify(options);
  
  if (imageTemplateCache.has(key)) {
    return imageTemplateCache.get(key);
  }
  
  const result = imageTemplate(options);
  imageTemplateCache.set(key, result);
  return result;
}
```

## Migration from Python Version

If you're migrating from the Python version, the JavaScript API is identical:

```python
# Python (before)
from canonicalwebteam import image_template

html = image_template(
    url="https://example.com/image.jpg",
    alt="Product image",
    width=800,
    height=600,
    fill=True
)
```

```javascript
// JavaScript (after)
import { imageTemplate } from '@canonical/image-template';

const html = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Product image',
  width: 800,
  height: 600,
  fill: true
});
```

The only differences are:
- JavaScript uses object parameter instead of named parameters
- `e_sharpen` becomes `eSharpen` (camelCase)
- Boolean values use JavaScript syntax (`true`/`false` instead of `True`/`False`)

## Troubleshooting

### Common Issues

1. **Module not found**: Ensure the package is installed and the import path is correct
2. **TypeScript errors**: Make sure `image_template.d.ts` is included in your project
3. **SSR issues**: The library works in both browser and Node.js environments
4. **Build errors**: Check your bundler configuration for proper module resolution

### Debug Mode

```javascript
// Enable debug logging
const html = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Debug image',
  width: 800
});

console.log('Generated HTML:', html);
```

For more examples and advanced usage, see the test files:
- `test_js_node.js` - Node.js examples
- `test_js_implementation.html` - Browser examples