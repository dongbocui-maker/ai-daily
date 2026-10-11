// Offline built-page check. No requests to live services.
// node tests/check-lmarena-page.mjs DIST_DIR CANDIDATE_JSON EVIDENCE_DIR
// PLAYWRIGHT_CHROMIUM_EXECUTABLE may select an already installed Chromium.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import { chromium } from 'playwright';

const [distArg, candidateArg, evidenceArg] = process.argv.slice(2);
assert(distArg && candidateArg && evidenceArg, 'Expected DIST_DIR CANDIDATE_JSON EVIDENCE_DIR');
const dist = path.resolve(distArg);
const candidate = JSON.parse(fs.readFileSync(candidateArg, 'utf8'));
fs.mkdirSync(evidenceArg, { recursive: true });
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
const server = http.createServer((req, res) => {
  let pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
  if (pathname.endsWith('/')) pathname += 'index.html';
  const file = path.resolve(dist, '.' + pathname);
  if (!file.startsWith(dist + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {
    res.writeHead(404).end(); return;
  }
  res.setHeader('Content-Type', types[path.extname(file)] ?? 'application/octet-stream');
  fs.createReadStream(file).pipe(res);
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const origin = `http://127.0.0.1:${server.address().port}`;
let browser;
try {
  browser = await chromium.launch({ headless: true,
    executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined });
  const page = await browser.newPage();
  await page.route('**/*', route => route.request().url().startsWith(origin)
    ? route.continue() : route.abort());
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  const checks = [];
  for (const viewport of [{ width: 1440, height: 1000 }, { width: 390, height: 844 }]) {
    await page.setViewportSize(viewport);
    const response = await page.goto(origin + '/lmarena/', { waitUntil: 'networkidle' });
    assert.equal(response.status(), 200);
    assert.equal(await page.locator('.rank-row').count(), 50);
    assert.equal(await page.locator('.rank-delta.base').count(), 50);
    assert.equal(await page.locator('.exit-chip').count(), 0);
    assert.deepEqual(await page.locator('.rank-name').allTextContents(), candidate.models.map(m => m.name));
    const main = await page.locator('main').innerText();
    for (const value of [candidate.snapshotDate, candidate.fetchedAt, candidate.sourceUpdatedAt,
      '文本总榜（风格控制）', '不计算与旧快照的升降', '10:30']) assert(main.includes(value), value);
    assert.equal((main.match(/Arena rating/g) || []).length, 51); // 50 rows + methodology
    assert(!main.includes('NaN'));
    assert(!main.includes('27 个评测维度'));
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > innerWidth);
    assert.equal(overflow, false, `Horizontal overflow at ${viewport.width}px`);
    await page.screenshot({ path: path.join(evidenceArg, `arena-${viewport.width}.png`), fullPage: true });
    checks.push({ viewport, rows: 50, baselineRows: 50, exitedModels: 0, horizontalOverflow: overflow });
  }
  assert.deepEqual(errors, []);
  const result = { ok: true, snapshotDate: candidate.snapshotDate, sourceUpdatedAt: candidate.sourceUpdatedAt,
    sourceSha256: candidate.sourceSha256, checks, pageErrors: errors };
  fs.writeFileSync(path.join(evidenceArg, 'page-check.json'), JSON.stringify(result, null, 2) + '\n');
  console.log(JSON.stringify(result, null, 2));
} finally {
  if (browser) await browser.close();
  await new Promise(resolve => server.close(resolve));
}
