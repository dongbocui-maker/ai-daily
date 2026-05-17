#!/usr/bin/env node
// fetch-original-texts.mjs
// 抓取 src/data/reads/*.json 里的 originalUrl，把英文原文保存成 markdown
// 输出到 obsidian-export/reads/*.md（覆盖之前的中文精读输出）
//
// 抓取策略：
//   - HTML：用 Readability 提取正文 + Turndown 转 markdown
//   - PDF：用 pdftotext 转纯文本
//   - 走 mihomo 代理（127.0.0.1:7890）
//   - 失败的源（如 Stratechery 付费墙）输出占位 markdown
//
// 用法：
//   node scripts/fetch-original-texts.mjs            # 抓全部
//   node scripts/fetch-original-texts.mjs <slug>     # 抓单篇
//
// 状态记录：obsidian-export/_status.json

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execSync, spawnSync } from 'node:child_process';
import { HttpsProxyAgent } from 'https-proxy-agent';

import { JSDOM, VirtualConsole } from 'jsdom';
import { Readability } from '@mozilla/readability';
import TurndownService from 'turndown';
import { chromium } from 'playwright';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const READS_SRC = path.join(REPO_ROOT, 'src', 'data', 'reads');
const OUT_DIR = path.join(REPO_ROOT, 'obsidian-export', 'reads');
const STATUS_FILE = path.join(REPO_ROOT, 'obsidian-export', '_status.json');

// ============ 代理配置 ============

const PROXY_URL = process.env.HTTPS_PROXY || process.env.https_proxy || 'http://127.0.0.1:7890';
let proxyAgent = null;
try {
  proxyAgent = new HttpsProxyAgent(PROXY_URL);
} catch {
  /* 没装 https-proxy-agent 也能跑，只是不走代理 */
}

// ============ 已知会失败的源（直接输出占位）============

const PAYWALL_DOMAINS = ['stratechery.com'];
const ANTIBOT_DOMAINS = ['mckinsey.com'];  // 高级反爬，无法程序报取

function isPaywalled(url) {
  return PAYWALL_DOMAINS.some((d) => url.includes(d));
}
function isAntibot(url) {
  return ANTIBOT_DOMAINS.some((d) => url.includes(d));
}

// ============ 工具函数 ============

function ensureDir(d) {
  fs.mkdirSync(d, { recursive: true });
}

function escapeYaml(s) {
  if (s == null) return '';
  return `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

function yamlArray(arr) {
  if (!arr || arr.length === 0) return ' []';
  return '\n' + arr.map((x) => `  - ${escapeYaml(x)}`).join('\n');
}

function formatTags(tags) {
  if (!Array.isArray(tags)) return ' []';
  return yamlArray(tags.map((t) => t.replace(/\s+/g, '-')));
}

// ============ 抓取 HTML ============

async function fetchUrl(url, timeoutMs = 30000) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, {
      signal: controller.signal,
      agent: proxyAgent,  // node-fetch style; native fetch ignores this
      headers: {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/pdf,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
      },
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const contentType = resp.headers.get('content-type') || '';
    const buf = Buffer.from(await resp.arrayBuffer());
    return { contentType, buf, ok: true };
  } finally {
    clearTimeout(timer);
  }
}

// Node 22 native fetch 不识别 agent 参数。用 undici 的 dispatcher 或 curl 兜底。
// 简化：直接用 curl（已确认 mihomo 在 7890 listen）
function fetchViaCurl(url, opts = {}) {
  const tmpFile = `/tmp/fetch-${Date.now()}-${Math.random().toString(36).slice(2)}.bin`;
  const maxTime = opts.maxTime || 180;  // 默认 3 分钟（大 PDF 用）
  const useHttp1 = opts.http1 || false;
  const useChromeHeaders = opts.chromeHeaders || false;
  const args = [
    '-fsSL',
    '-x', PROXY_URL,
    '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    '-H', 'Accept: text/html,application/xhtml+xml,application/pdf,*/*;q=0.9',
    '-H', 'Accept-Language: en-US,en;q=0.9',
    '-H', 'Accept-Encoding: gzip, deflate, br',
    '--compressed',
    '--max-time', String(maxTime),
    '-o', tmpFile,
    '-w', '%{content_type}',
  ];
  if (useHttp1) args.push('--http1.1');
  if (useChromeHeaders) {
    // 加上完整的 Chrome 请求头，绕过 OpenAI 等 403
    args.push(
      '-H', 'sec-ch-ua: "Chromium";v="131", "Not_A Brand";v="24", "Google Chrome";v="131"',
      '-H', 'sec-ch-ua-mobile: ?0',
      '-H', 'sec-ch-ua-platform: "macOS"',
      '-H', 'sec-fetch-dest: document',
      '-H', 'sec-fetch-mode: navigate',
      '-H', 'sec-fetch-site: none',
      '-H', 'sec-fetch-user: ?1',
      '-H', 'upgrade-insecure-requests: 1',
    );
  }
  args.push(url);

  try {
    const result = spawnSync('curl', args, { encoding: 'utf-8' });
    if (result.status !== 0) {
      throw new Error(`curl exit ${result.status}: ${result.stderr?.slice(0, 200)}`);
    }
    const buf = fs.readFileSync(tmpFile);
    const contentType = result.stdout || '';
    return { contentType, buf, ok: true };
  } finally {
    if (fs.existsSync(tmpFile)) fs.unlinkSync(tmpFile);
  }
}

// 针对不同源选择最佳 fetch 策略
async function fetchForUrl(url) {
  const host = new URL(url).hostname;

  // PDF 可能很大 -> 加长 timeout
  if (url.endsWith('.pdf')) {
    return fetchViaCurl(url, { maxTime: 300 });
  }

  // McKinsey 走代理 HTTP/2 报错，不走代理直连
  if (host.includes('mckinsey.com')) {
    return await fetchViaPlaywright(url, { useProxy: false });
  }
  // OpenAI 对 curl 返 403，需要完整 Chromium fingerprint，走代理
  if (host.includes('openai.com')) {
    return await fetchViaPlaywright(url);
  }

  return fetchViaCurl(url);
}

// Playwright fallback。对于对 curl 返 403 / TLS fingerprint 验证严格的站点。
const sharedBrowsers = { proxied: null, direct: null };
async function getSharedBrowser(useProxy = true) {
  const key = useProxy ? 'proxied' : 'direct';
  if (sharedBrowsers[key]) return sharedBrowsers[key];
  const launchOpts = {
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage'],
  };
  if (useProxy) launchOpts.proxy = { server: PROXY_URL };
  sharedBrowsers[key] = await chromium.launch(launchOpts);
  return sharedBrowsers[key];
}
async function fetchViaPlaywright(url, opts = {}) {
  const useProxy = opts.useProxy !== false;
  const browser = await getSharedBrowser(useProxy);
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    viewport: { width: 1440, height: 900 },
    locale: 'en-US',
  });
  const page = await ctx.newPage();
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForTimeout(3000);
    const html = await page.content();
    return { contentType: 'text/html; charset=utf-8', buf: Buffer.from(html, 'utf-8'), ok: true };
  } finally {
    await ctx.close();
  }
}
async function closeSharedBrowser() {
  for (const key of ['proxied', 'direct']) {
    if (sharedBrowsers[key]) {
      await sharedBrowsers[key].close();
      sharedBrowsers[key] = null;
    }
  }
}

// ============ HTML → Markdown ============

const turndown = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced',
  bulletListMarker: '-',
});

// 去掉常见噪音
turndown.remove(['script', 'style', 'noscript', 'iframe']);

function htmlToMarkdown(html, url) {
  const virtualConsole = new VirtualConsole();
  virtualConsole.on('error', () => {});  // 吞掉 CSS 解析错误
  const dom = new JSDOM(html, { url, virtualConsole });
  const reader = new Readability(dom.window.document);
  const article = reader.parse();
  if (!article || !article.content) {
    throw new Error('Readability 提取失败（可能是付费墙或动态加载）');
  }
  const md = turndown.turndown(article.content);
  return {
    title: article.title || '',
    byline: article.byline || '',
    length: article.length || 0,
    excerpt: article.excerpt || '',
    markdown: md.trim(),
  };
}

// ============ PDF → text ============

function pdfToText(buf) {
  const tmpPdf = `/tmp/pdf-${Date.now()}.pdf`;
  fs.writeFileSync(tmpPdf, buf);
  try {
    const txt = execSync(`pdftotext -layout "${tmpPdf}" -`, { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 });
    return txt.trim();
  } finally {
    if (fs.existsSync(tmpPdf)) fs.unlinkSync(tmpPdf);
  }
}

// ============ Frontmatter 构建 ============

function buildFrontmatter(data, extra = {}) {
  const { slug, savedDate, publishDate, titleZh, titleEn, author, authorTitle, originalUrl, tags, source, audio } = data;
  const fm = [];
  fm.push('---');
  if (titleEn) fm.push(`title: ${escapeYaml(titleEn)}`);
  else if (titleZh) fm.push(`title: ${escapeYaml(titleZh)}`);
  if (titleZh) fm.push(`title_zh: ${escapeYaml(titleZh)}`);
  if (author) fm.push(`author: ${escapeYaml(author)}`);
  if (authorTitle) fm.push(`author_title: ${escapeYaml(authorTitle)}`);
  if (publishDate) fm.push(`publish_date: ${publishDate}`);
  if (savedDate) fm.push(`saved_date: ${savedDate}`);
  if (originalUrl) fm.push(`original_url: ${escapeYaml(originalUrl)}`);
  if (slug) fm.push(`slug: ${escapeYaml(slug)}`);
  if (source) fm.push(`source: ${escapeYaml(source)}`);
  if (audio?.url) fm.push(`audio_url: ${escapeYaml(audio.url)}`);
  if (extra.fetchStatus) fm.push(`fetch_status: ${escapeYaml(extra.fetchStatus)}`);
  if (extra.fetchedAt) fm.push(`fetched_at: ${escapeYaml(extra.fetchedAt)}`);
  if (extra.fetchType) fm.push(`fetch_type: ${escapeYaml(extra.fetchType)}`);
  if (extra.contentLength != null) fm.push(`content_length: ${extra.contentLength}`);
  fm.push(`tags:${formatTags(tags)}`);
  fm.push('---');
  return fm.join('\n');
}

// ============ 单篇处理 ============

async function processOne(data) {
  const { slug, originalUrl, titleZh, titleEn } = data;
  console.log(`[${slug}] ${originalUrl}`);

  // Paywall / Antibot 直接占位
  if (isPaywalled(originalUrl) || isAntibot(originalUrl)) {
    const isPw = isPaywalled(originalUrl);
    const status = isPw ? 'paywall_skipped' : 'antibot_skipped';
    const reason = isPw
      ? `⚠️ 此文来自付费墙网站（${new URL(originalUrl).hostname}），无法自动抓取全文。`
      : `⚠️ 此文来自反爬严格的企业站点（${new URL(originalUrl).hostname}），服务器拒绝自动抓取。`;
    return {
      slug,
      status,
      url: originalUrl,
      markdown: [
        buildFrontmatter(data, { fetchStatus: status, fetchedAt: new Date().toISOString(), fetchType: 'placeholder' }),
        '',
        `# ${titleEn || titleZh}`,
        '',
        `> ${reason}`,
        '',
        `**原文链接**：[${originalUrl}](${originalUrl})`,
        '',
        '请手动访问原网址复制全文，用同名文件覆盖此占位。',
        '',
      ].join('\n'),
    };
  }

  try {
    const { contentType, buf } = await fetchForUrl(originalUrl);
    const isPdf = contentType.includes('application/pdf') || originalUrl.endsWith('.pdf');

    if (isPdf) {
      const text = pdfToText(buf);
      if (!text || text.length < 200) {
        throw new Error(`PDF 提取的文本太短（${text.length} 字节）`);
      }
      const fm = buildFrontmatter(data, {
        fetchStatus: 'ok',
        fetchedAt: new Date().toISOString(),
        fetchType: 'pdf',
        contentLength: text.length,
      });
      const md = [
        fm,
        '',
        `# ${titleEn || titleZh}`,
        '',
        `> 📄 原始 PDF：[${originalUrl}](${originalUrl})`,
        '> ',
        `> 此文由 pdftotext 从 PDF 转换而来——文字内容保留，图表 / 表格 / 排版可能丢失。`,
        '',
        '---',
        '',
        '```',
        text,
        '```',
        '',
      ].join('\n');
      return { slug, status: 'ok', type: 'pdf', length: text.length, markdown: md };
    }

    // HTML
    const html = buf.toString('utf-8');
    const article = htmlToMarkdown(html, originalUrl);
    if (article.length < 500) {
      throw new Error(`Readability 提取的正文太短（${article.length} 字符），可能未识别正文`);
    }
    const fm = buildFrontmatter(data, {
      fetchStatus: 'ok',
      fetchedAt: new Date().toISOString(),
      fetchType: 'html',
      contentLength: article.length,
    });
    const md = [
      fm,
      '',
      `# ${article.title || titleEn || titleZh}`,
      '',
      article.byline ? `*${article.byline}*` : '',
      '',
      `> 🔗 原文：[${originalUrl}](${originalUrl})`,
      '',
      '---',
      '',
      article.markdown,
      '',
    ].filter(Boolean).join('\n');
    return { slug, status: 'ok', type: 'html', length: article.length, markdown: md };
  } catch (e) {
    const errMsg = e.message || String(e);
    console.error(`  ❌ ${errMsg}`);
    const md = [
      buildFrontmatter(data, { fetchStatus: 'error', fetchedAt: new Date().toISOString(), fetchType: 'placeholder' }),
      '',
      `# ${titleEn || titleZh}`,
      '',
      `> ❌ 抓取失败：${errMsg}`,
      '',
      `**原文链接**：[${originalUrl}](${originalUrl})`,
      '',
      '请手动访问原网址保存全文。',
      '',
    ].join('\n');
    return { slug, status: 'error', error: errMsg, url: originalUrl, markdown: md };
  }
}

// ============ 主流程 ============

async function main() {
  ensureDir(OUT_DIR);

  const arg = process.argv[2];
  let files = fs.readdirSync(READS_SRC).filter((f) => f.endsWith('.json')).sort();
  if (arg) files = files.filter((f) => f.includes(arg));

  const status = { fetchedAt: new Date().toISOString(), items: [] };
  let ok = 0, err = 0, paywall = 0, antibot = 0;

  for (const filename of files) {
    const data = JSON.parse(fs.readFileSync(path.join(READS_SRC, filename), 'utf-8'));
    const result = await processOne(data);

    const outName = filename.replace(/\.json$/, '.md');
    fs.writeFileSync(path.join(OUT_DIR, outName), result.markdown, 'utf-8');

    status.items.push({
      slug: result.slug,
      status: result.status,
      type: result.type,
      length: result.length,
      error: result.error,
      url: result.url || data.originalUrl,
    });

    if (result.status === 'ok') ok++;
    else if (result.status === 'paywall_skipped') paywall++;
    else if (result.status === 'antibot_skipped') antibot++;
    else err++;

    // 礼貌延迟
    await new Promise((r) => setTimeout(r, 1500));
  }

  await closeSharedBrowser();
  fs.writeFileSync(STATUS_FILE, JSON.stringify(status, null, 2));

  console.log('');
  console.log('═══════════════════════════════════════');
  console.log(`✅ 成功:     ${ok}`);
  console.log(`💰 付费墙:   ${paywall}`);
  console.log(`🤖 反爬拦截: ${antibot}`);
  console.log(`❌ 失败:     ${err}`);
  console.log(`📂 输出:   ${OUT_DIR}`);
  console.log(`📊 状态:   ${STATUS_FILE}`);
}

main().catch((e) => {
  console.error('FATAL:', e);
  process.exit(1);
});
