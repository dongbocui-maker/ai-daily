import { chromium } from 'playwright';
import fs from 'node:fs';

const browser = await chromium.launch({
  executablePath: '/root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome',
  proxy: { server: 'http://127.0.0.1:7890' },
  args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
});
const ctx = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
});
const page = await ctx.newPage();
await page.goto('https://www.mckinsey.com/capabilities/people-and-organization/our-insights/escaping-the-pilot-trap-building-hr-for-the-agentic-era', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(5000);

const assets = [
  ['article.pdf', '/~/media/mckinsey/business%20functions/people%20and%20organizational%20performance/our%20insights/escaping%20the%20pilot%20trap%20building%20hr%20for%20the%20agentic%20era/escaping-the-pilot-trap-building-hr-for-the-agentic-era.pdf'],
  ['ex1.svgz', '/~/media/mckinsey/business%20functions/people%20and%20organizational%20performance/our%20insights/escaping%20the%20pilot%20trap%20building%20hr%20for%20the%20agentic%20era/hragentic_ex%201.svgz'],
  ['ex2.svgz', '/~/media/mckinsey/business%20functions/people%20and%20organizational%20performance/our%20insights/escaping%20the%20pilot%20trap%20building%20hr%20for%20the%20agentic%20era/hragentic_ex%202.svgz'],
  ['ex3.svgz', '/~/media/mckinsey/business%20functions/people%20and%20organizational%20performance/our%20insights/escaping%20the%20pilot%20trap%20building%20hr%20for%20the%20agentic%20era/hragentic_ex%203.svgz'],
];
for (const [name, path] of assets) {
  try {
    const b64 = await page.evaluate(async (p) => {
      const r = await fetch(p, { credentials: 'include' });
      if (!r.ok) return 'HTTP:' + r.status;
      const buf = await r.arrayBuffer();
      let bin = '';
      const bytes = new Uint8Array(buf);
      const chunk = 0x8000;
      for (let i = 0; i < bytes.length; i += chunk) {
        bin += String.fromCharCode.apply(null, bytes.subarray(i, i + chunk));
      }
      return btoa(bin);
    }, path);
    if (b64.startsWith('HTTP:')) { console.log(name, b64); continue; }
    fs.writeFileSync('/tmp/mck-assets/' + name, Buffer.from(b64, 'base64'));
    console.log(name, 'OK', Buffer.from(b64, 'base64').length);
  } catch (e) { console.log(name, 'ERR', e.message.slice(0, 100)); }
}
await browser.close();
