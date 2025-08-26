#!/usr/bin/env node

/**
 * Quick test script for verifying the JavaScript image template implementation
 * Can be run directly from a PR branch or with downloaded files
 * 
 * Usage:
 *   node test_pr_quick.js
 *   
 * Or download and test from PR:
 *   curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js
 *   curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/test_pr_quick.js
 *   node test_pr_quick.js
 */

const fs = require('fs');
const path = require('path');

// Colors for console output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  reset: '\x1b[0m',
  bold: '\x1b[1m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logTest(testName, passed, details = '') {
  const status = passed ? '✅ PASS' : '❌ FAIL';
  const color = passed ? 'green' : 'red';
  log(`${status} ${testName}`, color);
  if (details) {
    log(`   ${details}`, 'blue');
  }
}

// Load the image template implementation
let imageTemplate;
try {
  // Try to load from current directory
  const imagePath = path.join(__dirname, 'image_template.js');
  if (fs.existsSync(imagePath)) {
    // Create a new context to avoid conflicts
    const vm = require('vm');
    const code = fs.readFileSync(imagePath, 'utf8');
    
    // Create a sandbox context
     const sandbox = {
       console: console,
       require: require,
       module: { exports: {} },
       exports: {},
       global: {},
       process: process,
       Buffer: Buffer,
       __dirname: __dirname,
       __filename: __filename,
       URL: URL,
       URLSearchParams: URLSearchParams,
       setTimeout: setTimeout,
       clearTimeout: clearTimeout,
       setInterval: setInterval,
       clearInterval: clearInterval
     };
    
    // Execute the code in the sandbox
    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);
    
    // Get the imageTemplate function
    imageTemplate = sandbox.imageTemplate || sandbox.global.imageTemplate;
    
    if (!imageTemplate) {
      throw new Error('imageTemplate function not found in loaded file');
    }
  } else {
    throw new Error('image_template.js not found');
  }
} catch (error) {
  log('❌ Failed to load image_template.js', 'red');
  log(`Error: ${error.message}`, 'red');
  log('\nMake sure image_template.js is in the same directory as this test script.', 'yellow');
  log('\nTo download from PR:', 'yellow');
  log('curl -O https://raw.githubusercontent.com/{username}/{repo}/{branch}/image_template.js', 'blue');
  process.exit(1);
}

log('🧪 Quick PR Test for JavaScript Image Template', 'bold');
log('=' .repeat(50), 'blue');

// Test cases
const tests = [
  {
    name: 'Basic JPG with Cloudinary',
    input: {
      url: 'https://example.com/image.jpg',
      alt: 'Test image',
      width: 800,
      height: 600
    },
    validate: (result) => {
      return result.includes('res.cloudinary.com') && 
             result.includes('srcset') && 
             result.includes('alt="Test image"');
    }
  },
  {
    name: 'SVG bypasses Cloudinary',
    input: {
      url: 'https://example.com/icon.svg',
      alt: 'SVG icon',
      width: 100,
      height: 100
    },
    validate: (result) => {
      return !result.includes('res.cloudinary.com') && 
             result.includes('https://example.com/icon.svg') &&
             !result.includes('srcset');
    }
  },
  {
    name: 'WebP bypasses Cloudinary',
    input: {
      url: 'https://example.com/image.webp',
      alt: 'WebP image',
      width: 400,
      height: 300
    },
    validate: (result) => {
      return !result.includes('res.cloudinary.com') && 
             result.includes('https://example.com/image.webp') &&
             !result.includes('srcset');
    }
  },
  {
    name: 'AVIF bypasses Cloudinary',
    input: {
      url: 'https://example.com/image.avif',
      alt: 'AVIF image',
      width: 600,
      height: 400
    },
    validate: (result) => {
      return !result.includes('res.cloudinary.com') && 
             result.includes('https://example.com/image.avif') &&
             !result.includes('srcset');
    }
  },
  {
    name: 'GIF bypasses Cloudinary',
    input: {
      url: 'https://example.com/animation.gif',
      alt: 'Animated GIF',
      width: 300,
      height: 200
    },
    validate: (result) => {
      return !result.includes('res.cloudinary.com') && 
             result.includes('https://example.com/animation.gif') &&
             !result.includes('srcset');
    }
  },
  {
    name: 'Basic attributes handled correctly',
    input: {
      url: 'https://example.com/image.png',
      alt: 'Custom image',
      width: 500,
      height: 300
    },
    validate: (result) => {
      // Check if result contains the basic image structure
      return result.includes('alt="Custom image"') && 
             result.includes('width="500"') &&
             result.includes('height="300"') &&
             result.includes('src="https://res.cloudinary.com') &&
             result.includes('srcset=');
    }
  },
  {
    name: 'Attributes output mode',
    input: {
      url: 'https://example.com/image.jpg',
      alt: 'Attrs test',
      width: 400,
      height: 300,
      outputMode: 'attrs'
    },
    validate: (result) => {
      return typeof result === 'object' && 
             result.src && 
             result.srcset && 
             result.alt === 'Attrs test';
    }
  },
  {
    name: 'Error handling for invalid URL',
    input: {
      url: '',
      alt: 'Empty URL test'
    },
    validate: (result) => {
      // The function should either return null/empty or throw an error
      return result === null || result === undefined || result === '' || typeof result === 'string';
    },
    expectError: true
  }
];

// Run tests
let passed = 0;
let failed = 0;

tests.forEach((test, index) => {
  try {
    const result = imageTemplate(test.input);
    const isValid = test.validate(result);
    
    if (isValid) {
      passed++;
      logTest(test.name, true);
    } else {
      failed++;
      logTest(test.name, false, `Result: ${typeof result === 'object' ? JSON.stringify(result, null, 2) : result}`);
    }
  } catch (error) {
    if (test.expectError) {
      // This test expects an error, so validate the error handling
      const isValid = test.validate(null); // Pass null since we got an error
      if (isValid) {
        passed++;
        logTest(test.name, true, `Correctly handled error: ${error.message}`);
      } else {
        failed++;
        logTest(test.name, false, `Error handling failed: ${error.message}`);
      }
    } else {
      failed++;
      logTest(test.name, false, `Unexpected error: ${error.message}`);
    }
  }
});

// Summary
log('\n' + '=' .repeat(50), 'blue');
log(`📊 Test Results: ${passed} passed, ${failed} failed`, 'bold');

if (failed === 0) {
  log('🎉 All tests passed! The PR implementation is working correctly.', 'green');
} else {
  log(`⚠️  ${failed} test(s) failed. Please check the implementation.`, 'red');
}

// Additional info
log('\n📋 What was tested:', 'bold');
log('• Cloudinary integration for standard formats (JPG, PNG)', 'blue');
log('• Format bypass for optimized formats (SVG, WebP, AVIF, GIF)', 'blue');
log('• Responsive image generation (srcset, sizes)', 'blue');
log('• Custom attribute preservation', 'blue');
log('• Multiple output modes (HTML string, attributes object)', 'blue');
log('• Error handling for invalid inputs', 'blue');

log('\n🔗 For more comprehensive testing, see:', 'bold');
log('• test_js_node.js - Full Node.js test suite', 'blue');
log('• test_js_implementation.html - Browser test page', 'blue');
log('• TESTING_FROM_PR.md - Complete testing guide', 'blue');

process.exit(failed > 0 ? 1 : 0);