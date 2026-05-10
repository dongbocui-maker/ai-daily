#!/usr/bin/env node
/**
 * Capture each slide from creative-deck.html using html2canvas via CDP.
 * Connects to the already-running browser, captures each slide, saves as PNG.
 */

const fs = require('fs');
const path = require('path');

const OUT_DIR = path.join(__dirname, '..', 'output', 'slides-png');
fs.mkdirSync(OUT_DIR, { recursive: true });

const PAGE_URL = 'http://localhost:8765/creative-deck.html';

// Find browser WebSocket endpoint from Chrome's DevTools port
// The browser tool manages Chrome; find the debugging URL
async function findBrowserWSEndpoint() {
  try {
    const resp = await fetch('http://127.0.0.1:9222/json/version');
    const data = await resp.json();
    return data.webSocketDebuggerUrl;
  } catch (e) {
    // Try alternative ports
    for (const port of [9223, 9224, 9225, 9226, 9227, 9228, 9229]) {
      try {
        const resp = await fetch(`http://127.0.0.1:${port}/json/version`);
        const data = await resp.json();
        return data.webSocketDebuggerUrl;
      } catch (_) {}
    }
    return null;
  }
}

async function main() {
  const wsUrl = await findBrowserWSEndpoint();
  if (!wsUrl) {
    console.error('No browser CDP endpoint found. Make sure Chrome is running with --remote-debugging-port=9222');
    process.exit(1);
  }

  console.log('Connected to browser via CDP:', wsUrl);

  const puppeteer = require('puppeteer');
  const browser = await puppeteer.connect({ browserWSEndpoint: wsUrl });
  const pages = await browser.pages();
  const page = pages[0];
  await page.goto(PAGE_URL, { waitUntil: 'networkidle0', timeout: 30000 });

  // Inject html2canvas
  await page.addScriptTag({ url: 'https://html2canvas.hertzen.com/dist/html2canvas.min.js' });
  await page.waitForFunction(() => typeof window.html2canvas !== 'undefined', { timeout: 10000 });

  const slideCount = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log(`Found ${slideCount} slides`);

  for (let i = 0; i < slideCount; i++) {
    const dataUrl = await page.evaluate((idx) => {
      const slide = document.querySelectorAll('.slide')[idx];
      slide.scrollIntoView({ block: 'start' });
      return html2canvas(slide, { scale: 2, backgroundColor: '#0a0a0a' }).then(c => c.toDataURL('image/png'));
    }, i);

    const base64 = dataUrl.replace(/^data:image\/png;base64,/, '');
    const buf = Buffer.from(base64, 'base64');
    const outPath = path.join(OUT_DIR, `slide-${String(i + 1).padStart(2, '0')}.png`);
    fs.writeFileSync(outPath, buf);
    console.log(`  [${String(i + 1).padStart(2, '0')}] ${(buf.length / 1024).toFixed(1)} KB → ${outPath}`);
  }

  await browser.disconnect();
  console.log(`\nDone. ${slideCount} slides → ${OUT_DIR}`);
}

main().catch(err => { console.error(err); process.exit(1); });
