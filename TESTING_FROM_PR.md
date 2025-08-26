# Testing JavaScript Image Template from GitHub PR

This guide explains how to test the JavaScript image template implementation directly from a GitHub Pull Request before it's merged.

## Method 1: Direct File Download from GitHub PR

### Step 1: Get Raw File URLs
From your PR, you can access the raw files directly:

```
# Replace {username}, {repo}, and {branch} with actual values
https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js
https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.d.ts
https://raw.githubusercontent.com/{username}/{repo}/{branch}/test_js_implementation.html
```

### Step 2: Use in HTML (Browser Testing)
```html
<!DOCTYPE html>
<html>
<head>
    <title>Testing Image Template from PR</title>
</head>
<body>
    <!-- Load directly from GitHub -->
    <script src="https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js"></script>
    
    <div id="test-container"></div>
    
    <script>
        // Test the implementation
        const html = imageTemplate({
            url: 'https://example.com/test.jpg',
            alt: 'Test image',
            width: 800,
            height: 600
        });
        
        document.getElementById('test-container').innerHTML = html;
        console.log('Generated HTML:', html);
    </script>
</body>
</html>
```

### Step 3: Download and Test Locally
```bash
# Download the files
curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js
curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.d.ts
curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/test_js_node.js

# Test with Node.js
node test_js_node.js
```

## Method 2: Clone PR Branch

### Step 1: Clone the PR Branch
```bash
# Clone the repository
git clone https://github.com/{username}/{repo}.git
cd {repo}

# Checkout the PR branch
git fetch origin pull/{PR_NUMBER}/head:pr-{PR_NUMBER}
git checkout pr-{PR_NUMBER}
```

### Step 2: Test the Implementation
```bash
# Run Node.js tests
node test_js_node.js

# Open browser test
open test_js_implementation.html
# or
python3 -m http.server 8000
# Then visit http://localhost:8000/test_js_implementation.html
```

## Method 3: NPM Installation from Git Branch

### Step 1: Install from Git Branch
```bash
# Install directly from the PR branch
npm install git+https://github.com/{username}/{repo}.git#{branch-name}

# Or using a specific commit
npm install git+https://github.com/{username}/{repo}.git#{commit-hash}
```

### Step 2: Use in Your Project
```javascript
// ES Modules
import { imageTemplate } from '@canonical/image-template';

// CommonJS
const { imageTemplate } = require('@canonical/image-template');

// Test it
const result = imageTemplate({
    url: 'https://example.com/image.jpg',
    alt: 'Test image',
    width: 800,
    height: 600
});

console.log(result);
```

## Method 4: GitHub Codespaces/Gitpod

### GitHub Codespaces
1. Go to your PR on GitHub
2. Click "Code" → "Codespaces" → "Create codespace on {branch}"
3. Once loaded, run:
```bash
node test_js_node.js
```

### Gitpod
1. Prefix your PR URL with `https://gitpod.io/#`
2. Example: `https://gitpod.io/#https://github.com/{username}/{repo}/pull/{PR_NUMBER}`
3. Run tests in the online IDE

## Method 5: JSFiddle/CodePen Testing

### JSFiddle
1. Go to [JSFiddle](https://jsfiddle.net/)
2. In the JavaScript panel, add:
```javascript
// Load the script dynamically
const script = document.createElement('script');
script.src = 'https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js';
script.onload = function() {
    // Test the implementation
    const html = imageTemplate({
        url: 'https://example.com/test.jpg',
        alt: 'Test image',
        width: 800,
        height: 600
    });
    
    document.body.innerHTML = html;
    console.log('Generated HTML:', html);
};
document.head.appendChild(script);
```

### CodePen
Similar approach in CodePen's JavaScript panel.

## Method 6: Testing in Different Frameworks

### React Testing
```bash
# Create a test React app
npx create-react-app test-image-template
cd test-image-template

# Download the files
curl -o src/imageTemplate.js https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js

# Use in a component
# src/App.js
import './imageTemplate.js';

function App() {
  const imageHtml = window.imageTemplate({
    url: 'https://example.com/test.jpg',
    alt: 'Test image',
    width: 800,
    height: 600
  });
  
  return (
    <div dangerouslySetInnerHTML={{ __html: imageHtml }} />
  );
}

export default App;
```

### Vue.js Testing
```bash
# Create a test Vue app
npm create vue@latest test-image-template
cd test-image-template
npm install

# Download the file to public folder
curl -o public/imageTemplate.js https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js

# Use in a component
# src/components/TestImage.vue
<template>
  <div v-html="imageHtml"></div>
</template>

<script>
export default {
  data() {
    return {
      imageHtml: ''
    }
  },
  mounted() {
    // Load the script
    const script = document.createElement('script');
    script.src = '/imageTemplate.js';
    script.onload = () => {
      this.imageHtml = window.imageTemplate({
        url: 'https://example.com/test.jpg',
        alt: 'Test image',
        width: 800,
        height: 600
      });
    };
    document.head.appendChild(script);
  }
}
</script>
```

## Verification Checklist

When testing from a PR, verify these key features:

- [ ] **Format Bypass**: SVG, WebP, AVIF, GIF files bypass Cloudinary
- [ ] **Cloudinary Integration**: JPG, PNG files use Cloudinary with srcset
- [ ] **Responsive Images**: srcset and sizes attributes are generated
- [ ] **Custom Attributes**: Additional HTML attributes are preserved
- [ ] **Error Handling**: Invalid inputs are handled gracefully
- [ ] **Output Modes**: Both 'html' and 'attrs' modes work
- [ ] **TypeScript Support**: Type definitions work correctly
- [ ] **Browser Compatibility**: Works in different browsers
- [ ] **Node.js Compatibility**: Works in Node.js environment

## Common Issues and Solutions

### CORS Issues
If you encounter CORS errors when loading from GitHub:
```javascript
// Use a CORS proxy
const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
const scriptUrl = proxyUrl + 'https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js';
```

### Cache Issues
GitHub raw files are cached. To get the latest version:
```
# Add a cache-busting parameter
https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js?v=123
```

### Module Loading Issues
If you have module loading issues:
```html
<!-- For ES modules -->
<script type="module">
  import('./image_template.js').then(module => {
    // Use the module
  });
</script>
```

## Example PR Testing URLs

Replace these placeholders with actual values:
- `{username}`: GitHub username (e.g., `canonical`)
- `{repo}`: Repository name (e.g., `canonicalwebteam.image-template`)
- `{branch}`: PR branch name (e.g., `feature/js-implementation`)
- `{PR_NUMBER}`: Pull request number (e.g., `42`)

Example:
```
https://raw.githubusercontent.com/canonical/canonicalwebteam.image-template/feature/js-implementation/image_template.js
```

This allows you to thoroughly test the JavaScript implementation before the PR is merged!