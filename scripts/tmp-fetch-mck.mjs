import { chromium } from 'playwright';
import fs from 'node:fs';

const url = 'https://www.mckinsey.com/capabilities/people-and-organization/our-insights/escaping-the-pilot-trap-building-hr-for-the-agentic-era';
const browser = await chromium.launch({
  executablePath: '/root/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome',
  proxy: { server: 'http://127.0.0.1:7890' },
  args: ['--disable-blink-features=AutomationControlled', '--no-sandbox'],
});
const ctx = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
  viewport: { width: 1440, height: 900 },
  locale: 'en-US',
});
const page = await ctx.newPage();
try {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(8000);
  const html = await page.content();
  fs.writeFileSync('/tmp/mck-hr.html', html);
  console.log('saved', html.length, 'title:', await page.title());
} catch (e) {
  console.error('ERR', e.message);
}
await browser.close();
