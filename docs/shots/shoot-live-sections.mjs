import { chromium } from '/root/.npm/_npx/e41f203b7505f1fb/node_modules/playwright-core/index.mjs';
const exe = '/root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome';
const outDir = '/root/.openclaw/workspace/projects/ai-daily/docs/shots';
const pages = [
  ['reads','https://aidigest.club/reads/'],
  ['github','https://aidigest.club/github/'],
  ['lmarena','https://aidigest.club/lmarena/'],
  ['archive','https://aidigest.club/archive/'],
  ['learn','https://aidigest.club/learn/'],
];
const browser = await chromium.launch({ executablePath: exe, args: ['--no-sandbox'] });
// desktop
const dctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
for (const [name, url] of pages) {
  const p = await dctx.newPage();
  await p.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
  await p.screenshot({ path: `${outDir}/live-sec-${name}-desktop.png` });
  await p.close();
}
// mobile (one representative)
const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true });
const mp = await mctx.newPage();
await mp.goto('https://aidigest.club/reads/', { waitUntil: 'networkidle', timeout: 30000 });
await mp.screenshot({ path: `${outDir}/live-sec-reads-mobile.png` });
await browser.close();
console.log('done');
