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

async function translateText(
  text: string,
  cache: TranslationCache,
  llm: { apiBase: string; apiKey: string; model: string } | null,
): Promise<string> {
  if (!text.trim()) return '';
  if (cache[text]) return cache[text];
  if (!llm) return ''; // 离线模式：返回空，前端 fallback 显示原文

  try {
    const res = await fetch(`${llm.apiBase.replace(/\/$/, '')}/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${llm.apiKey}`,
      },
      body: JSON.stringify({
        model: llm.model,
        temperature: 0.1,
        messages: [
          {
            role: 'system',
            content: '你是一名英中翻译。把给定的 GitHub 仓库 description 翻译成中文。规则：\n1. 简洁自然，不超过原文长度\n2. 保留专业术语英文（API、SDK、CLI、LLM、RAG 等）\n3. 不加任何解释或前缀\n4. 直接输出中文译文',
          },
          { role: 'user', content: text },
        ],
      }),
    });
    if (!res.ok) {
      console.warn(`[translate] HTTP ${res.status}: ${await res.text()}`);
      return '';
    }
    const data = await res.json();
    const zh = (data.choices?.[0]?.message?.content ?? '').trim();
    if (zh) cache[text] = zh;
    return zh;
  } catch (err) {
    console.warn(`[translate] fail:`, err);
    return '';
  }
}

async function translateBoard(
  repos: GitHubRepo[],
  cache: TranslationCache,
  llm: { apiBase: string; apiKey: string; model: string } | null,
): Promise<GitHubRepo[]> {
  // 串行限速（避免 rate limit）
  for (const repo of repos) {
    if (repo.description) {
      repo.description_zh = await translateText(repo.description, cache, llm);
    }
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

  const llm = (process.env.LLM_API_KEY && process.env.LLM_API_BASE)
    ? {
        apiBase: process.env.LLM_API_BASE,
        apiKey: process.env.LLM_API_KEY,
        model: process.env.LLM_MODEL ?? 'deepseek-v4-flash',
      }
    : null;

  if (skipTranslate) {
    console.log('[main] --no-translate: 跳过翻译');
  } else if (!llm) {
    console.log('[main] LLM 未配置 (.env 缺 LLM_API_KEY)，跳过翻译');
  } else {
    console.log(`[main] 使用 ${llm.model} 翻译，cache 路径 ${TRANSLATION_CACHE_PATH}`);
  }

  const cache = loadTranslationCache();
  const info = getDateInfo();
  const dataRoot = resolve(__dirname, '../src/data/github');

  // === 日榜 ===
  console.log('[daily] fetching trending...');
  const dailyRaw = await fetchTrending('daily');
  console.log(`[daily] got ${dailyRaw.length} repos, enriching...`);
  const daily = await enrichBatch(dailyRaw);
  if (llm && !skipTranslate) await translateBoard(daily, cache, llm);
  writeJson(`${dataRoot}/daily/${info.date}.json`, buildBoard(daily));
  console.log(`[daily] saved → daily/${info.date}.json (general=${daily.length}, ai=${daily.filter(isAIRelated).length})`);

  if (!onlyDaily) {
    // === 周榜 ===
    console.log('[weekly] fetching...');
    const weeklyRaw = await fetchTrending('weekly');
    const weekly = await enrichBatch(weeklyRaw);
    if (llm && !skipTranslate) await translateBoard(weekly, cache, llm);
    writeJson(`${dataRoot}/weekly/${info.yearWeek}.json`, buildBoard(weekly));
    console.log(`[weekly] saved → weekly/${info.yearWeek}.json`);

    // === 月榜 ===
    console.log('[monthly] fetching...');
    const monthlyRaw = await fetchTrending('monthly');
    const monthly = await enrichBatch(monthlyRaw);
    if (llm && !skipTranslate) await translateBoard(monthly, cache, llm);
    writeJson(`${dataRoot}/monthly/${info.yearMonth}.json`, buildBoard(monthly));
    console.log(`[monthly] saved → monthly/${info.yearMonth}.json`);

    // === 年榜：双 tab ===
    console.log('[yearly] fetching newborn...');
    const newborn = await fetchSearch(`created:>${info.year}-01-01 stars:>500`, 50);
    if (llm && !skipTranslate) await translateBoard(newborn, cache, llm);

    console.log('[yearly] fetching fastest growing...');
    // 用 pushed 最近 + stars 高 作为「今年活跃 + 高热度」近似
    const fastest = await fetchSearch(`pushed:>${info.year}-01-01 stars:>10000`, 50);
    if (llm && !skipTranslate) await translateBoard(fastest, cache, llm);

    writeJson(`${dataRoot}/yearly/${info.year}.json`, {
      newborn: buildBoard(newborn),
      fastest_growing: buildBoard(fastest),
    } satisfies YearlyBoardData);
    console.log(`[yearly] saved → yearly/${info.year}.json`);
  }

  saveTranslationCache(cache);
  console.log(`[done] cache size: ${Object.keys(cache).length}`);
}

main().catch((err) => {
  console.error('[fatal]', err);
  process.exit(1);
});
