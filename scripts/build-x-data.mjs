#!/usr/bin/env node

import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);

const DEFAULT_PREPARE = '/root/skills/follow-builders/scripts/prepare-digest.js';
const DEFAULT_OUT_DIR = 'src/data/x/daily';
const DEFAULT_PUBLIC_DIR = 'public/x/data';

function parseArgs(argv) {
  const args = { input: '', outDir: DEFAULT_OUT_DIR, publicDir: DEFAULT_PUBLIC_DIR, date: '', sourcePath: DEFAULT_PREPARE };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--input') args.input = argv[++i];
    else if (arg === '--out-dir') args.outDir = argv[++i];
    else if (arg === '--public-dir') args.publicDir = argv[++i];
    else if (arg === '--date') args.date = argv[++i];
    else if (arg === '--prepare') args.sourcePath = argv[++i];
    else if (arg === '--help' || arg === '-h') {
      console.log(`Usage: node scripts/build-x-data.mjs [--input /tmp/fb.json] [--date YYYY-MM-DD] [--out-dir src/data/x/daily] [--public-dir public/x/data]\n\nWithout --input, calls /root/skills/follow-builders/scripts/prepare-digest.js.\nNever calls generate-feed.js.`);
      process.exit(0);
    }
  }
  return args;
}

async function loadSource(args) {
  if (args.input) {
    return JSON.parse(await readFile(resolve(args.input), 'utf-8'));
  }
  if (!existsSync(args.sourcePath)) {
    throw new Error(`prepare-digest.js not found: ${args.sourcePath}`);
  }
  const { stdout, stderr } = await execFileAsync('node', [args.sourcePath], {
    cwd: dirname(args.sourcePath),
    maxBuffer: 20 * 1024 * 1024,
    env: { ...process.env, HTTPS_PROXY: process.env.HTTPS_PROXY || 'http://127.0.0.1:7890' },
  });
  if (stderr?.trim()) console.error(stderr.trim());
  return JSON.parse(stdout);
}

function localDate(iso = new Date().toISOString()) {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(new Date(iso));
}

function stripNoise(text = '') {
  return String(text)
    .replace(/Speaker\s+\d+\s*\|\s*\d{2}:\d{2}\s*-\s*\d{2}:\d{2}/gi, '')
    .replace(/\bCHAT GPT\b/g, 'ChatGPT')
    .replace(/https:\/\/t\.co\/\S+/g, '')
    .replace(/\s+/g, ' ')
    .replace(/\s+([,.!?;:])/g, '$1')
    .trim();
}

function normalizeDate(value) {
  if (!value) return null;
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return null;
  return date.toISOString();
}

function assertSourceShape(source) {
  const missing = ['x', 'podcasts', 'blogs'].filter((key) => !Array.isArray(source[key]));
  if (missing.length) {
    throw new Error(`Follow Builders source missing array field(s): ${missing.join(', ')}`);
  }
}

function truncate(text = '', max = 220) {
  const cleaned = stripNoise(text);
  if (cleaned.length <= max) return cleaned;
  return `${cleaned.slice(0, max - 1).trim()}…`;
}

function firstSentence(text = '', max = 96) {
  const cleaned = stripNoise(text);
  const sentence = cleaned.split(/(?<=[.!?。！？])\s+/)[0] || cleaned;
  return truncate(sentence, max);
}

function scoreTweet(tweet) {
  return (tweet.likes || 0) + (tweet.retweets || 0) * 4 + (tweet.replies || 0) * 2;
}

const TAG_RULES = [
  ['Claude', /claude|anthropic/i],
  ['OpenAI', /openai|chatgpt|gpt/i],
  ['Agent', /agent|agents|agentic/i],
  ['Coding', /codex|code|coding|developer|sdk|github/i],
  ['Product', /product|app|feature|platform|vercel/i],
  ['Eval', /eval|benchmark|metr|quality/i],
  ['Startup', /yc|founder|startup|hiring|pm/i],
  ['Research', /science|research|discover|model/i],
  ['Infrastructure', /database|infrastructure|fusion|platform/i],
];

function inferTags(text) {
  const tags = [];
  for (const [tag, re] of TAG_RULES) {
    if (re.test(text) && !tags.includes(tag)) tags.push(tag);
  }
  return tags.slice(0, 4);
}

function zhInsight(text, kind, sourceName = 'Builder') {
  const lower = text.toLowerCase();
  const subject = sourceName.replace(/^The\s+/i, '').slice(0, 32);
  if (/openai|chatgpt|gpt/.test(lower)) return `${subject} 的信号指向 OpenAI 能力继续产品化；重点不只是模型发布，而是记忆、工具链和应用入口如何改变用户工作流。`;
  if (/claude|anthropic/.test(lower) && /code|codex|developer|sdk|engineering/.test(lower)) return `${subject} 把 Claude/AI Coding 放在工程生产力语境里；值得看的是模型参与真实开发的比例、质量门槛和组织流程变化。`;
  if (/claude|anthropic/.test(lower)) return `${subject} 相关动态显示 Claude/Anthropic 生态仍在扩张；短期看产品采用，长期看它能否形成稳定的开发者与企业工作流。`;
  if (/codex|code|coding|sdk|developer/.test(lower)) return `${subject} 的内容强调 AI Coding 正从编辑器插件走向可编程能力层，SDK、技能和集成会成为下一轮差异化。`;
  if (/agent|agents|agentic/.test(lower)) return `${subject} 提到的 agent 信号说明市场正在从概念转向任务闭环；可靠性、评测和可控集成会决定能否规模化。`;
  if (/eval|benchmark|metr|quality/.test(lower)) return `${subject} 触及评测/质量问题，这是 AI 产品化的底层约束；没有可信评测，企业部署和用户信任都会受限。`;
  if (/hiring|pm|founder|startup|yc/.test(lower)) return `${subject} 反映 AI 创业与人才结构继续重组，产品、工程、增长角色的边界正在被重新定义。`;
  if (kind === 'podcast') return `${subject} 这类长访谈比短消息更能暴露技术路线和战略假设，适合作为判断行业方向的高信号材料。`;
  if (kind === 'blog') return `${subject} 的工程长文提供实现约束和复盘经验，比发布稿更适合判断能力边界、质量风险和落地成本。`;
  return `${subject} 这条信号虽不一定是大新闻，但能反映 builders 对产品方向、技术栈或市场节奏的实时判断。`;
}

function makeXItems(builders = []) {
  const tweets = [];
  for (const builder of builders) {
    for (const tweet of builder.tweets || []) {
      const text = stripNoise(tweet.text || '');
      if (text.length < 36) continue;
      const tagCount = inferTags(`${builder.name || ''} ${builder.bio || ''} ${text}`).length;
      if (tagCount === 0 && text.length < 80) continue;
      tweets.push({ builder, tweet, text, score: scoreTweet(tweet), tagCount });
    }
  }

  return tweets
    .sort((a, b) => (b.tagCount - a.tagCount) || b.score - a.score || new Date(b.tweet.createdAt || 0) - new Date(a.tweet.createdAt || 0))
    .slice(0, 12)
    .map(({ builder, tweet, text, score }) => ({
      id: `x-${tweet.id}`,
      kind: 'x',
      source: 'X',
      sourceName: builder.name || builder.handle || 'X Builder',
      handle: builder.handle || '',
      title: `${builder.name || builder.handle}: ${firstSentence(text, 88)}`,
      summaryEn: truncate(text, 240),
      insightZh: zhInsight(text, 'x', builder.name || builder.handle || 'X Builder'),
      tags: inferTags(`${builder.name || ''} ${builder.bio || ''} ${text}`),
      url: tweet.url,
      publishedAt: normalizeDate(tweet.createdAt),
      metrics: {
        likes: tweet.likes || 0,
        retweets: tweet.retweets || 0,
        replies: tweet.replies || 0,
        score,
      },
    }));
}

function makePodcastItems(podcasts = []) {
  return podcasts.slice(0, 3).map((podcast, index) => {
    const text = podcast.transcript || podcast.description || '';
    const tagText = `${podcast.name || ''} ${podcast.title || ''}`;
    return {
      id: `podcast-${podcast.guid || index}`,
      kind: 'podcast',
      source: 'Podcast',
      sourceName: podcast.name || 'Podcast',
      title: podcast.title || podcast.name || 'Podcast episode',
      summaryEn: truncate(text, 260),
      insightZh: zhInsight(`${podcast.title || ''} ${text.slice(0, 1200)}`, 'podcast', podcast.name || 'Podcast'),
      tags: inferTags(tagText),
      url: podcast.url,
      publishedAt: normalizeDate(podcast.publishedAt),
    };
  });
}

function makeBlogItems(blogs = []) {
  return blogs.slice(0, 6).map((blog, index) => {
    const text = blog.description || blog.content || '';
    const tagText = `${blog.name || ''} ${blog.title || ''} ${blog.description || ''}`;
    return {
      id: `blog-${index}-${Buffer.from(blog.url || blog.title || String(index)).toString('base64url').slice(0, 10)}`,
      kind: 'blog',
      source: 'Blog',
      sourceName: blog.name || blog.author || 'Blog',
      title: blog.title || blog.name || 'Blog post',
      summaryEn: truncate(text, 260),
      insightZh: zhInsight(`${blog.name || ''} ${blog.title || ''} ${text.slice(0, 1200)}`, 'blog', blog.name || blog.author || 'Blog'),
      tags: inferTags(tagText),
      url: blog.url,
      publishedAt: normalizeDate(blog.publishedAt),
      author: blog.author || '',
    };
  });
}

function buildSiteData(source, args) {
  assertSourceShape(source);
  const generatedAt = source.generatedAt || new Date().toISOString();
  const date = args.date || localDate(generatedAt);
  const xItems = makeXItems(source.x || []);
  const podcastItems = makePodcastItems(source.podcasts || []);
  const blogItems = makeBlogItems(source.blogs || []);
  const allItems = [...xItems, ...podcastItems, ...blogItems];
  const featured = [
    ...xItems.slice().sort((a, b) => (b.metrics?.score || 0) - (a.metrics?.score || 0)).slice(0, 2),
    ...podcastItems.slice(0, 1),
  ].filter(Boolean).slice(0, 3);

  if (Array.isArray(source.errors) && source.errors.length) {
    console.error(`Follow Builders source reported ${source.errors.length} non-fatal issue(s); keeping them in build logs only.`);
  }

  return {
    date,
    title: `Builder Signals · ${date}`,
    generatedAt,
    feedGeneratedAt: source.stats?.feedGeneratedAt || null,
    summary: `Follow Builders 今日捕捉到 ${source.stats?.totalTweets ?? xItems.length} 条 X 动态、${source.stats?.podcastEpisodes ?? podcastItems.length} 集播客、${source.stats?.blogPosts ?? blogItems.length} 篇博客；本站精选 ${allItems.length} 条高信号内容。`,
    stats: {
      xBuilders: source.stats?.xBuilders || source.x?.length || 0,
      totalTweets: source.stats?.totalTweets || 0,
      selectedXTweets: xItems.length,
      podcastEpisodes: source.stats?.podcastEpisodes || podcastItems.length,
      blogPosts: source.stats?.blogPosts || blogItems.length,
      selectedItems: allItems.length,
    },
    featured,
    sections: [
      { key: 'x', label: 'X Signals', description: '来自 builders / founders / researchers 的实时短信号。', items: xItems },
      { key: 'podcast', label: 'Podcasts', description: '长访谈与播客，适合判断技术路线和战略假设。', items: podcastItems },
      { key: 'blog', label: 'Blogs', description: '工程博客与长文，关注能力边界、复盘和落地经验。', items: blogItems },
    ],
  };
}

const args = parseArgs(process.argv.slice(2));
const source = await loadSource(args);
if (source.status !== 'ok') {
  throw new Error(`Follow Builders source status is not ok: ${source.status || 'unknown'}`);
}
const data = buildSiteData(source, args);
const outDir = resolve(args.outDir);
await mkdir(outDir, { recursive: true });
const outPath = resolve(outDir, `${data.date}.json`);
await writeFile(outPath, `${JSON.stringify(data, null, 2)}\n`);

const publicDir = resolve(args.publicDir);
await mkdir(publicDir, { recursive: true });
const publicDatePath = resolve(publicDir, `${data.date}.json`);
const publicLatestPath = resolve(publicDir, 'latest.json');
await writeFile(publicDatePath, `${JSON.stringify(data, null, 2)}\n`);
await writeFile(publicLatestPath, `${JSON.stringify(data, null, 2)}\n`);

console.log(JSON.stringify({
  status: 'ok',
  outPath,
  publicDatePath,
  publicLatestPath,
  date: data.date,
  items: data.stats.selectedItems,
}, null, 2));
