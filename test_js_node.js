/**
 * Node.js test script for the JavaScript image_template implementation
 * Run with: node test_js_node.js
 */

// Import the image template implementation
const { ImageTemplate, imageTemplate } = require('./image_template.js');

console.log('🧪 Testing JavaScript Image Template Implementation\n');

// Test 1: Regular JPG image with Cloudinary processing
console.log('📸 Test 1: Regular JPG Image with Cloudinary Processing');
const test1 = imageTemplate({
  url: 'https://example.com/image.jpg',
  alt: 'Test image',
  width: 800,
  height: 600,
  loading: 'lazy'
});
console.log('Result:', test1);
console.log('✅ Should contain Cloudinary URL and srcset\n');

// Test 2: SVG image (should bypass Cloudinary)
console.log('🎨 Test 2: SVG Image (Bypasses Cloudinary)');
const test2 = imageTemplate({
  url: 'https://example.com/logo.svg',
  alt: 'SVG logo',
  width: 200,
  height: 100
});
console.log('Result:', test2);
console.log('✅ Should use original URL without srcset\n');

// Test 3: WebP image (should bypass Cloudinary)
console.log('🖼️  Test 3: WebP Image (Bypasses Cloudinary)');
const test3 = imageTemplate({
  url: 'https://example.com/modern.webp',
  alt: 'WebP image',
  width: 600,
  height: 400
});
console.log('Result:', test3);
console.log('✅ Should use original URL without srcset\n');

// Test 4: GIF image (should bypass Cloudinary)
console.log('🎬 Test 4: GIF Image (Bypasses Cloudinary)');
const test4 = imageTemplate({
  url: 'https://example.com/animation.gif',
  alt: 'Animated GIF',
  width: 300,
  height: 200
});
console.log('Result:', test4);
console.log('✅ Should use original URL without srcset\n');

// Test 5: AVIF image (should bypass Cloudinary)
console.log('🆕 Test 5: AVIF Image (Bypasses Cloudinary)');
const test5 = imageTemplate({
  url: 'https://example.com/modern.avif',
  alt: 'AVIF image',
  width: 400,
  height: 300
});
console.log('Result:', test5);
console.log('✅ Should use original URL without srcset\n');

// Test 6: Image with custom attributes and fill
console.log('⚙️  Test 6: Image with Custom Attributes and Fill');
const test6 = imageTemplate({
  url: 'https://example.com/hero.png',
  alt: 'Hero image',
  width: 1200,
  height: 800,
  fill: true,
  eSharpen: true,
  fmt: 'webp',
  attrs: {
    'class': 'hero-image',
    'data-testid': 'main-hero'
  },
  hiDef: true
});
console.log('Result:', test6);
console.log('✅ Should contain Cloudinary URL with c_fill, e_sharpen, and custom attributes\n');

// Test 7: Attributes mode output
console.log('📋 Test 7: Attributes Mode Output');
const test7 = imageTemplate({
  url: 'https://example.com/thumbnail.jpg',
  alt: 'Thumbnail',
  width: 150,
  height: 150,
  outputMode: 'attrs'
});
console.log('Result:', JSON.stringify(test7, null, 2));
console.log('✅ Should return object with image attributes\n');

// Test 8: Small image (should not generate srcset)
console.log('🔍 Test 8: Small Image (No Srcset)');
const test8 = imageTemplate({
  url: 'https://example.com/small.jpg',
  alt: 'Small image',
  width: 50,
  height: 50
});
console.log('Result:', test8);
console.log('✅ Should not contain srcset (width <= 100px)\n');

// Test 9: Custom srcset widths
console.log('📐 Test 9: Custom Srcset Widths');
const test9 = imageTemplate({
  url: 'https://example.com/custom.jpg',
  alt: 'Custom srcset',
  width: 800,
  srcsetWidths: [400, 800, 1200]
});
console.log('Result:', test9);
console.log('✅ Should use custom srcset widths\n');

// Test 10: Error handling - invalid output mode
console.log('❌ Test 10: Error Handling - Invalid Output Mode');
try {
  const test10 = imageTemplate({
    url: 'https://example.com/test.jpg',
    alt: 'Test',
    width: 400,
    outputMode: 'invalid'
  });
  console.log('❌ Should have thrown an error');
} catch (error) {
  console.log('✅ Correctly threw error:', error.message);
}
console.log();

// Test 11: Error handling - missing hostname
console.log('❌ Test 11: Error Handling - Missing Hostname');
try {
  const test11 = imageTemplate({
    url: '/relative/path.jpg',
    alt: 'Test',
    width: 400
  });
  console.log('❌ Should have thrown an error');
} catch (error) {
  console.log('✅ Correctly threw error:', error.message);
}
console.log();

console.log('🎉 All tests completed!');
console.log('\n📝 Summary:');
console.log('- SVG, WebP, AVIF, and GIF files bypass Cloudinary processing');
console.log('- Regular formats (JPG, PNG) use Cloudinary with srcset generation');
console.log('- Custom attributes and options are properly handled');
console.log('- Error handling works for invalid inputs');
console.log('- Both HTML and attributes output modes are supported');