/**
 * GitHub Trending + Search API 抓取
 *
 * 输出：
 *   src/data/github/daily/YYYY-MM-DD.json
 *   src/data/github/weekly/YYYY-WXX.json
 *   src/data/github/monthly/YYYY-MM.json
 *   src/data/github/yearly/YYYY.json   (双 tab：newborn / fastest-growing)
 *
 * 每个 JSON 包含 general (综合) 和 ai (AI 专题) 两个数组。
 */

import { writeFileSync, mkdirSync, existsSync, readFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as cheerio from 'cheerio';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ============ Types ============

export interface GitHubRepo {
  rank: number;
  name: string;            // owner/repo
  url: string;
  description: string;     // 原文（英文居多）
  description_zh?: string; // 翻译后中文
  features?: string[];     // 核心功能清单（AI 从 README 抽取）
  language?: string;
  stars: number;           // 当前 stars 总数
  stars_period?: number;   // 本期增量（trending 才有）
  forks?: number;
  topics?: string[];       // GitHub topics
  pushed_at?: string;      // ISO 时间
  created_at?: string;     // ISO 时间
}

export interface BoardData {
  general: GitHubRepo[];
  ai: GitHubRepo[];
}

export interface YearlyBoardData {
  newborn: BoardData;          // 今年新创建
  fastest_growing: BoardData;  // 今年 stars 增量最多
}

// ============ AI 专题过滤规则 ============

const AI_TOPICS = new Set([
  'ai', 'artificial-intelligence', 'machine-learning', 'ml', 'deep-learning',
  'llm', 'large-language-models', 'language-model', 'gpt', 'chatgpt',
  'agent', 'agents', 'ai-agents', 'autonomous-agents',
  'rag', 'embeddings', 'vector-database', 'vector-search',
  'transformer', 'transformers', 'pytorch', 'tensorflow',
  'computer-vision', 'cv', 'nlp', 'natural-language-processing',
  'diffusion', 'stable-diffusion', 'image-generation', 'text-to-image',
  'mcp', 'anthropic', 'openai', 'huggingface', 'langchain',
  'copilot', 'ai-coding', 'code-generation',
]);

const AI_KEYWORDS = [
  /\bAI\b/i, /\bLLM\b/i, /\bGPT\b/i, /\bRAG\b/i, /\bMCP\b/i,
  /\bagent[s]?\b/i, /\bcopilot\b/i,
  /machine\s*learning/i, /deep\s*learning/i, /neural\s*network/i,
  /natural\s*language/i, /computer\s*vision/i,
  /chatbot/i, /transformer/i, /diffusion/i, /embedding/i,
  /人工智能/, /大模型/, /智能体/, /机器学习/, /深度学习/,
];

function isAIRelated(repo: GitHubRepo): boolean {
  const topics = repo.topics ?? [];
  if (topics.some((t) => AI_TOPICS.has(t.toLowerCase()))) return true;
  const blob = `${repo.name} ${repo.description ?? ''}`;
  return AI_KEYWORDS.some((p) => p.test(blob));
}

// ============ GitHub Trending 爬虫 ============

export async function fetchTrending(since: 'daily' | 'weekly' | 'monthly'): Promise<GitHubRepo[]> {
  const url = `https://github.com/trending?since=${since}&spoken_language_code=`;
  const res = await fetch(url, {
    headers: {
      'User-Agent': 'Mozilla/5.0 ai-daily/1.0',
      'Accept-Language': 'en-US,en;q=0.9',
    },
  });
  if (!res.ok) throw new Error(`Trending HTTP ${res.status}`);
  const html = await res.text();
  const $ = cheerio.load(html);

  const repos: GitHubRepo[] = [];
  $('article.Box-row').each((i, el) => {
    const $el = $(el);
    const link = $el.find('h2 a').attr('href')?.trim();
    if (!link) return;
    const name = link.replace(/^\//, '');
    const description = $el.find('p').first().text().trim();
    const language = $el.find('[itemprop="programmingLanguage"]').first().text().trim() || undefined;

    // stars 总数 (第一个 svg-text 后)
    const numbers = $el.find('a.Link--muted').map((_, a) => $(a).text().trim().replace(/,/g, '')).get();
    const stars = parseInt(numbers[0] ?? '0', 10) || 0;
    const forks = parseInt(numbers[1] ?? '0', 10) || 0;

    // 本期增量 ("123 stars today" / "1,234 stars this week")
    const periodText = $el.find('.d-inline-block.float-sm-right').text().trim();
    const periodMatch = periodText.match(/([\d,]+)\s+stars/);
    const stars_period = periodMatch ? parseInt(periodMatch[1].replace(/,/g, ''), 10) : undefined;

    repos.push({
      rank: i + 1,
      name,
      url: `https://github.com${link}`,
      description,
      language,
      stars,
      stars_period,
      forks,
    });
  });
  return repos.slice(0, 25);
}

// ============ GitHub Search API ============

export async function fetchSearch(q: string, perPage = 50): Promise<GitHubRepo[]> {
  const params = new URLSearchParams({
    q,
    sort: 'stars',
    order: 'desc',
    per_page: String(perPage),
  });
  const headers: Record<string, string> = {
    'Accept': 'application/vnd.github+json',
    'X-GitHub-Api-Version': '2022-11-28',
    'User-Agent': 'ai-daily/1.0',
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  const res = await fetch(`https://api.github.com/search/repositories?${params}`, { headers });
  if (!res.ok) throw new Error(`Search API HTTP ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return (data.items ?? []).map((item: any, i: number): GitHubRepo => ({
    rank: i + 1,
    name: item.full_name,
    url: item.html_url,
    description: item.description ?? '',
    language: item.language ?? undefined,
    stars: item.stargazers_count,
    forks: item.forks_count,
    topics: item.topics ?? [],
    pushed_at: item.pushed_at,
    created_at: item.created_at,
  }));
}

// ============ 拓展 topics / created_at（trending 没返回这些，需要单独查 repo API）============

async function enrichRepo(repo: GitHubRepo): Promise<GitHubRepo> {
  if (repo.topics && repo.created_at) return repo;
  const headers: Record<string, string> = {
    'Accept': 'application/vnd.github+json',
    'User-Agent': 'ai-daily/1.0',
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }
  try {
    const res = await fetch(`https://api.github.com/repos/${repo.name}`, { headers });
    if (!res.ok) return repo;
    const data = await res.json();
    return {
      ...repo,
      topics: data.topics ?? [],
      pushed_at: data.pushed_at,
      created_at: data.created_at,
      forks: data.forks_count ?? repo.forks,
      stars: data.stargazers_count ?? repo.stars,
    };
  } catch {
    return repo;
  }
}

async function enrichBatch(repos: GitHubRepo[], concurrency = 5): Promise<GitHubRepo[]> {
  const out: GitHubRepo[] = [];
  for (let i = 0; i < repos.length; i += concurrency) {
    const batch = repos.slice(i, i + concurrency);
    const enriched = await Promise.all(batch.map(enrichRepo));
    out.push(...enriched);
    if (i + concurrency < repos.length) await new Promise((r) => setTimeout(r, 200));
  }
  return out;
}

// ============ README 与 Features 抽取 ============

const READMES_DIR = resolve(__dirname, '../src/data/github/_readmes');

async function fetchReadme(repoName: string): Promise<string | null> {
  const safe = repoName.replace('/', '__');
  const cachePath = `${READMES_DIR}/${safe}.md`;

  // 缓存检查（1 周内不重复拓）
  if (existsSync(cachePath)) {
    const stat = require('node:fs').statSync(cachePath);
    const ageMs = Date.now() - stat.mtimeMs;
    if (ageMs < 7 * 24 * 60 * 60 * 1000) {
      return readFileSync(cachePath, 'utf-8');
    }
  }

  const headers: Record<string, string> = {
    'Accept': 'application/vnd.github.raw',
    'User-Agent': 'ai-daily/1.0',
  };
  if (process.env.GITHUB_TOKEN) {
    headers['Authorization'] = `Bearer ${process.env.GITHUB_TOKEN}`;
  }

  try {
    const res = await fetch(`https://api.github.com/repos/${repoName}/readme`, { headers });
    if (!res.ok) return null;
    const text = await res.text();
    mkdirSync(READMES_DIR, { recursive: true });
    writeFileSync(cachePath, text);
    return text;
  } catch (err) {
    console.warn(`[readme] fail ${repoName}:`, err);
    return null;
  }
}

const FEATURES_CACHE_PATH = resolve(__dirname, '../src/data/github/_features.json');

interface FeaturesCache {
  // key: owner/repo, value: { features, sourceHash, ts }
  [repoName: string]: { features: string[]; sourceHash: string; ts: number };
}

function loadFeaturesCache(): FeaturesCache {
  if (!existsSync(FEATURES_CACHE_PATH)) return {};
  try { return JSON.parse(readFileSync(FEATURES_CACHE_PATH, 'utf-8')); } catch { return {}; }
}

function saveFeaturesCache(cache: FeaturesCache) {
  mkdirSync(dirname(FEATURES_CACHE_PATH), { recursive: true });
  writeFileSync(FEATURES_CACHE_PATH, JSON.stringify(cache, null, 2));
}

function simpleHash(s: string): string {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h << 5) - h + s.charCodeAt(i);
    h |= 0;
  }
  return h.toString(16);
}

const FEATURES_PROMPT = `你是一名 GitHub 项目分析师。基于下面的 README 摘要，抽取这个项目的 3-5 条核心功能 / 特性（features）。

要求：
1. 每条 1 句话，简洁有力，15-30 字
2. 保留专业术语英文（API、SDK、CLI、LLM、agent、framework 等）
3. 只列「真实存在」的功能，不要编造
4. 输出严格 JSON 数组，如 ["feature1", "feature2", ...]，不要任何前缀 / 后缀 / 代码块包裹
5. 如果 README 信息不足，返回你能确认的那几条，宁少勿编
6. 如果 README 是净贡献指南、安装说明主导，返回空数组 []

README 摘要：`;

async function extractFeatures(
  repoName: string,
  readme: string,
  cache: FeaturesCache,
  llm: LLMConfig | null,
): Promise<string[]> {
  if (!readme.trim()) return [];
  if (!llm) return [];

  const truncated = readme.slice(0, 3000); // 控制 input token
  const sourceHash = simpleHash(truncated);

  // 缓存命中：同一项目 README 未变则不重抽
  const cached = cache[repoName];
  if (cached && cached.sourceHash === sourceHash) {
    return cached.features;
  }

  try {
    const fullPrompt = FEATURES_PROMPT + truncated;
    const raw = llm.protocol === 'anthropic'
      ? await callAnthropic({ ...llm }, fullPrompt, 500)
      : await callOpenAI({ ...llm }, fullPrompt, 500);
    // 尝试解析 JSON 数组
    const trimmed = raw.trim().replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '');
    let features: string[] = [];
    try {
      const parsed = JSON.parse(trimmed);
      if (Array.isArray(parsed)) features = parsed.filter((x) => typeof x === 'string');
    } catch {
      // fallback: split bullet points
      features = trimmed
        .split('\n')
        .map((l) => l.replace(/^[-*\d.\s]+/, '').trim())
        .filter((l) => l.length > 5 && l.length < 100);
    }
    cache[repoName] = { features, sourceHash, ts: Date.now() };
    return features;
  } catch (err) {
    console.warn(`[features] fail ${repoName}:`, err instanceof Error ? err.message : err);
    return [];
  }
}

// ============ 翻译缓存 ============

const TRANSLATION_CACHE_PATH = resolve(__dirname, '../src/data/github/_translations.json');

interface TranslationCache {
  [originalText: string]: string;  // 原文 → 中文
}

function loadTranslationCache(): TranslationCache {
  if (!existsSync(TRANSLATION_CACHE_PATH)) return {};
  try {
    return JSON.parse(readFileSync(TRANSLATION_CACHE_PATH, 'utf-8'));
  } catch {
    return {};
  }
}

function saveTranslationCache(cache: TranslationCache) {
  mkdirSync(dirname(TRANSLATION_CACHE_PATH), { recursive: true });
  writeFileSync(TRANSLATION_CACHE_PATH, JSON.stringify(cache, null, 2));
}

type LLMProtocol = 'openai' | 'anthropic';

interface LLMConfig {
  apiBase: string;
  apiKey: string;
  model: string;
  protocol: LLMProtocol;
}

const SYSTEM_PROMPT = '你是一名英中翻译。把给定的 GitHub 仓库 description 翻译成中文。规则：\n1. 简洁自然，不超过原文长度\n2. 保留专业术语英文（API、SDK、CLI、LLM、RAG 等）\n3. 不加任何解释或前缀\n4. 直接输出中文译文';

async function callOpenAI(llm: LLMConfig, text: string, maxTokens = 200): Promise<string> {
  const res = await fetch(`${llm.apiBase.replace(/\/$/, '')}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${llm.apiKey}`,
    },
    body: JSON.stringify({
      model: llm.model,
      temperature: 0.1,
      max_tokens: maxTokens,
      messages: [
        { role: 'system', content: SYSTEM_PROMPT },
        { role: 'user', content: text },
      ],
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const data = await res.json();
  return (data.choices?.[0]?.message?.content ?? '').trim();
}

async function callAnthropic(llm: LLMConfig, text: string, maxTokens = 200): Promise<string> {
  const res = await fetch(`${llm.apiBase.replace(/\/$/, '')}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': llm.apiKey,
      'anthropic-version': '2023-06-01',
      Authorization: `Bearer ${llm.apiKey}`, // Azure 需要 Bearer
    },
    body: JSON.stringify({
      model: llm.model,
      max_tokens: maxTokens,
      system: SYSTEM_PROMPT,
      messages: [{ role: 'user', content: text }],
    }),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
  const data = await res.json();
  // Anthropic 响应格式：{ content: [{ type: 'text', text: '...' }] }
  const block = data.content?.[0];
  return (block?.text ?? '').trim();
}

async function translateText(
  text: string,
  cache: TranslationCache,
  llm: LLMConfig | null,
): Promise<string> {
  if (!text.trim()) return '';
  if (cache[text]) return cache[text];
  if (!llm) return ''; // 离线模式：返回空，前端 fallback 显示原文

  try {
    const zh = llm.protocol === 'anthropic'
      ? await callAnthropic(llm, text)
      : await callOpenAI(llm, text);
    if (zh) cache[text] = zh;
    return zh;
  } catch (err) {
    console.warn(`[translate] fail (${llm.protocol}):`, err instanceof Error ? err.message : err);
    return '';
  }
}

async function translateBoard(
  repos: GitHubRepo[],
  cache: TranslationCache,
  llm: LLMConfig | null,
): Promise<GitHubRepo[]> {
  // 串行限速（避免 rate limit）
  for (const repo of repos) {
    if (repo.description) {
      repo.description_zh = await translateText(repo.description, cache, llm);
    }
  }
  return repos;
}

async function enrichFeaturesBoard(
  repos: GitHubRepo[],
  cache: FeaturesCache,
  llm: LLMConfig | null,
): Promise<GitHubRepo[]> {
  // 串行不多并发调用避免 Azure rate limit
  for (const repo of repos) {
    const cachedEntry = cache[repo.name];
    // 缓存还在且不超过 30 天：直接复用
    if (cachedEntry && Date.now() - cachedEntry.ts < 30 * 24 * 60 * 60 * 1000) {
      repo.features = cachedEntry.features;
      continue;
    }
    const readme = await fetchReadme(repo.name);
    if (!readme) {
      repo.features = [];
      continue;
    }
    repo.features = await extractFeatures(repo.name, readme, cache, llm);
  }
  return repos;
}

// ============ 主流程 ============

function getDateInfo() {
  const now = new Date();
  const tz = 8 * 60; // 北京时间
  const offset = now.getTimezoneOffset() + tz;
  const cn = new Date(now.getTime() + offset * 60 * 1000);
  const y = cn.getFullYear();
  const m = String(cn.getMonth() + 1).padStart(2, '0');
  const d = String(cn.getDate()).padStart(2, '0');
  return {
    date: `${y}-${m}-${d}`,
    year: String(y),
    yearMonth: `${y}-${m}`,
    yearWeek: `${y}-W${String(getWeek(cn)).padStart(2, '0')}`,
  };
}

function getWeek(d: Date) {
  const target = new Date(d.valueOf());
  const dayNr = (d.getDay() + 6) % 7;
  target.setDate(target.getDate() - dayNr + 3);
  const firstThursday = target.valueOf();
  target.setMonth(0, 1);
  if (target.getDay() !== 4) {
    target.setMonth(0, 1 + ((4 - target.getDay()) + 7) % 7);
  }
  return 1 + Math.ceil((firstThursday - target.valueOf()) / 604800000);
}

function buildBoard(repos: GitHubRepo[]): BoardData {
  return {
    general: repos,
    ai: repos.filter(isAIRelated),
  };
}

function writeJson(path: string, data: unknown) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2));
}

async function main() {
  const args = process.argv.slice(2);
  const onlyDaily = args.includes('--daily-only');
  const skipTranslate = args.includes('--no-translate');

  // Auto-detect protocol: if LLM_PROTOCOL is set, use it; otherwise infer from URL
  const inferProtocol = (url: string): LLMProtocol => {
    if (/anthropic|claude/i.test(url)) return 'anthropic';
    return 'openai';
  };
  const llm: LLMConfig | null = (process.env.LLM_API_KEY && process.env.LLM_API_BASE)
    ? {
        apiBase: process.env.LLM_API_BASE,
        apiKey: process.env.LLM_API_KEY,
        model: process.env.LLM_MODEL ?? 'claude-opus-4-7',
        protocol: (process.env.LLM_PROTOCOL as LLMProtocol | undefined) ?? inferProtocol(process.env.LLM_API_BASE),
      }
    : null;

  const skipFeatures = args.includes('--no-features');

  if (skipTranslate) {
    console.log('[main] --no-translate: 跳过翻译');
  } else if (!llm) {
    console.log('[main] LLM 未配置 (.env 缺 LLM_API_KEY)，跳过翻译');
  } else {
    console.log(`[main] 使用 ${llm.model} (${llm.protocol}) 翻译+features，cache 路径 ${TRANSLATION_CACHE_PATH}`);
  }

  const cache = loadTranslationCache();
  const featuresCache = loadFeaturesCache();
  const info = getDateInfo();
  const dataRoot = resolve(__dirname, '../src/data/github');

  // === 日榜 ===
  console.log('[daily] fetching trending...');
  const dailyRaw = await fetchTrending('daily');
  console.log(`[daily] got ${dailyRaw.length} repos, enriching...`);
  const daily = await enrichBatch(dailyRaw);
  if (llm && !skipTranslate) await translateBoard(daily, cache, llm);
  if (llm && !skipFeatures) await enrichFeaturesBoard(daily, featuresCache, llm);
  writeJson(`${dataRoot}/daily/${info.date}.json`, buildBoard(daily));
  console.log(`[daily] saved → daily/${info.date}.json (general=${daily.length}, ai=${daily.filter(isAIRelated).length})`);

  if (!onlyDaily) {
    // === 周榜 ===
    console.log('[weekly] fetching...');
    const weeklyRaw = await fetchTrending('weekly');
    const weekly = await enrichBatch(weeklyRaw);
    if (llm && !skipTranslate) await translateBoard(weekly, cache, llm);
    if (llm && !skipFeatures) await enrichFeaturesBoard(weekly, featuresCache, llm);
    writeJson(`${dataRoot}/weekly/${info.yearWeek}.json`, buildBoard(weekly));
    console.log(`[weekly] saved → weekly/${info.yearWeek}.json`);

    // === 月榜 ===
    console.log('[monthly] fetching...');
    const monthlyRaw = await fetchTrending('monthly');
    const monthly = await enrichBatch(monthlyRaw);
    if (llm && !skipTranslate) await translateBoard(monthly, cache, llm);
    if (llm && !skipFeatures) await enrichFeaturesBoard(monthly, featuresCache, llm);
    writeJson(`${dataRoot}/monthly/${info.yearMonth}.json`, buildBoard(monthly));
    console.log(`[monthly] saved → monthly/${info.yearMonth}.json`);

    // === 年榜：双 tab ===
    console.log('[yearly] fetching newborn...');
    const newborn = await fetchSearch(`created:>${info.year}-01-01 stars:>500`, 50);
    if (llm && !skipTranslate) await translateBoard(newborn, cache, llm);
    if (llm && !skipFeatures) await enrichFeaturesBoard(newborn, featuresCache, llm);

    console.log('[yearly] fetching fastest growing...');
    const fastest = await fetchSearch(`pushed:>${info.year}-01-01 stars:>10000`, 50);
    if (llm && !skipTranslate) await translateBoard(fastest, cache, llm);
    if (llm && !skipFeatures) await enrichFeaturesBoard(fastest, featuresCache, llm);

    writeJson(`${dataRoot}/yearly/${info.year}.json`, {
      newborn: buildBoard(newborn),
      fastest_growing: buildBoard(fastest),
    } satisfies YearlyBoardData);
    console.log(`[yearly] saved → yearly/${info.year}.json`);
  }

  saveTranslationCache(cache);
  saveFeaturesCache(featuresCache);
  console.log(`[done] translations=${Object.keys(cache).length}, features=${Object.keys(featuresCache).length}`);
}

main().catch((err) => {
  console.error('[fatal]', err);
  process.exit(1);
});
