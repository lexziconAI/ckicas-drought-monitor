#!/usr/bin/env node
/**
 * ADVANCED COMPONENT RENDERING TEST
 * Tests if React components are actually rendering after JavaScript execution
 */

const puppeteer = require('puppeteer');

async function testComponentRendering() {
  console.log('🧪 Testing Advanced Component Rendering...');

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    const page = await browser.newPage();

    // Set timeout for page load
    await page.setDefaultTimeout(30000);

    console.log('  📄 Loading dashboard...');
    await page.goto('http://localhost:3000', { waitUntil: 'networkidle0' });

    // Wait for React to hydrate
    await page.waitForTimeout(2000);

    console.log('  🔍 Checking for component elements...');

    // Test for critical components
    const tests = [
      { selector: '[class*="grid"]', name: 'Grid Layout' },
      { selector: 'h2', name: 'Headers' },
      { selector: '[class*="portfolio"]', name: 'Portfolio Panel' },
      { selector: '[class*="performance"]', name: 'Performance Panel' },
      { selector: '[class*="activity"]', name: 'Activity Panel' },
      { selector: 'button', name: 'Interactive Elements' },
      { selector: 'canvas', name: 'Canvas Elements' }
    ];

    let passedTests = 0;

    for (const test of tests) {
      try {
        const element = await page.$(test.selector);
        if (element) {
          console.log(`    ✅ ${test.name} found`);
          passedTests++;
        } else {
          console.log(`    ❌ ${test.name} not found`);
        }
      } catch (error) {
        console.log(`    ⚠️ ${test.name} error: ${error.message}`);
      }
    }

    // Check for JavaScript errors
    const jsErrors = [];
    page.on('pageerror', (error) => {
      jsErrors.push(error.message);
    });

    // Wait a bit more for any async errors
    await page.waitForTimeout(1000);

    console.log(`\n📊 Test Results:`);
    console.log(`  ✅ Components found: ${passedTests}/${tests.length}`);
    console.log(`  ❌ JavaScript errors: ${jsErrors.length}`);

    if (jsErrors.length > 0) {
      console.log('  🚨 JavaScript Errors:');
      jsErrors.forEach((error, i) => {
        console.log(`    ${i + 1}. ${error}`);
      });
    }

    // Overall assessment
    const successRate = passedTests / tests.length;
    if (successRate >= 0.7 && jsErrors.length === 0) {
      console.log('\n🎉 DASHBOARD RENDERING TEST: PASSED');
      console.log('🌐 Dashboard should be fully functional!');
    } else if (successRate >= 0.5) {
      console.log('\n⚠️ DASHBOARD RENDERING TEST: PARTIAL SUCCESS');
      console.log('Some components may not be loading properly');
    } else {
      console.log('\n❌ DASHBOARD RENDERING TEST: FAILED');
      console.log('Critical rendering issues detected');
    }

  } catch (error) {
    console.error('❌ Component rendering test failed:', error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// Run the test
testComponentRendering().catch(console.error);