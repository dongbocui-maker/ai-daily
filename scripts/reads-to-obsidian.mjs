#!/usr/bin/env node
// reads-to-obsidian.mjs
// 把 src/data/reads/*.json 转成 Obsidian 友好的 markdown
// 输出到 obsidian-export/reads/*.md（仓库根目录的 obsidian-export 目录）
// 每个 markdown 包含：YAML frontmatter（含 tags）+ 音频链接 + 原文 summaryZh + 附录（insight/keyPoints/quotes/原文 URL）

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// repo root 就是 projects/ai-daily/（GitHub 上单 repo）
const REPO_ROOT = path.resolve(__dirname, '..');
const READS_SRC = path.join(REPO_ROOT, 'src', 'data', 'reads');
const OBSIDIAN_OUT = path.join(REPO_ROOT, 'obsidian-export', 'reads');

// ---- 工具函数 ----

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function escapeYamlString(s) {
  if (s == null) return '';
  // YAML 安全：包成双引号 + 转义 " 和 \
  return `"${String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"')}"`;
}

function yamlArray(arr) {
  if (!arr || arr.length === 0) return '[]';
  return '\n' + arr.map((x) => `  - ${escapeYamlString(x)}`).join('\n');
}

// 把站内 /reads/slug/ 链接转成 Obsidian 双链 [[slug]]
function rewriteInternalLinks(md) {
  if (!md) return md;
  // 匹配 [text](/reads/some-slug/) 或 [text](/reads/some-slug)
  return md.replace(/\[([^\]]+)\]\(\/reads\/([a-z0-9-]+)\/?\)/gi, (_m, text, slug) => {
    return `[[${slug}|${text}]]`;
  });
}

function formatTagsForYaml(tags) {
  if (!tags || !Array.isArray(tags)) return '[]';
  // Obsidian tags 要 kebab-case，移除空格和特殊字符
  return yamlArray(tags.map((t) => t.replace(/\s+/g, '-')));
}

// ---- 主转换器 ----

function convertJsonToMarkdown(data) {
  const {
    slug,
    savedDate,
    publishDate,
    titleZh,
    titleEn,
    author,
    authorTitle,
    originalUrl,
    tags,
    summary,
    keyPoints,
    insight,
    summaryZh,
    quotes,
    source,
    audio,
  } = data;

  // ---- YAML frontmatter ----
  const fm = [];
  fm.push('---');
  fm.push(`title: ${escapeYamlString(titleZh)}`);
  if (titleEn) fm.push(`title_en: ${escapeYamlString(titleEn)}`);
  if (author) fm.push(`author: ${escapeYamlString(author)}`);
  if (authorTitle) fm.push(`author_title: ${escapeYamlString(authorTitle)}`);
  if (publishDate) fm.push(`publish_date: ${publishDate}`);
  if (savedDate) fm.push(`saved_date: ${savedDate}`);
  if (originalUrl) fm.push(`original_url: ${escapeYamlString(originalUrl)}`);
  if (slug) fm.push(`slug: ${escapeYamlString(slug)}`);
  if (source) fm.push(`source: ${escapeYamlString(source)}`);
  if (audio?.url) fm.push(`audio_url: ${escapeYamlString(audio.url)}`);
  if (audio?.duration_seconds) {
    const mm = Math.floor(audio.duration_seconds / 60);
    const ss = String(Math.round(audio.duration_seconds % 60)).padStart(2, '0');
    fm.push(`audio_duration: "${mm}:${ss}"`);
  }
  fm.push(`tags:${formatTagsForYaml(tags)}`);
  fm.push('---');

  // ---- 正文 ----
  const lines = [];
  lines.push(fm.join('\n'));
  lines.push('');

  // 标题
  lines.push(`# ${titleZh}`);
  lines.push('');

  // 元信息块
  const metaParts = [];
  if (author) metaParts.push(`**作者**：${author}${authorTitle ? `（${authorTitle}）` : ''}`);
  if (publishDate) metaParts.push(`**发表**：${publishDate}`);
  if (originalUrl) metaParts.push(`**原文**：[${originalUrl}](${originalUrl})`);
  if (audio?.url) {
    const dur = audio.duration_seconds
      ? `${Math.floor(audio.duration_seconds / 60)}:${String(Math.round(audio.duration_seconds % 60)).padStart(2, '0')}`
      : '';
    metaParts.push(`**音频**：[${dur ? `播客 ${dur}` : '播客'}](${audio.url})`);
  }
  if (metaParts.length > 0) {
    lines.push(metaParts.join(' · '));
    lines.push('');
    lines.push('---');
    lines.push('');
  }

  // 主体——原文 summaryZh
  if (summaryZh) {
    lines.push(rewriteInternalLinks(summaryZh).trim());
    lines.push('');
  }

  // ---- 附录 ----
  lines.push('---');
  lines.push('');
  lines.push('## 附录');
  lines.push('');

  // TL;DR
  if (summary) {
    lines.push('### TL;DR');
    lines.push('');
    lines.push(summary.trim());
    lines.push('');
  }

  // Key Points
  if (keyPoints && keyPoints.length > 0) {
    lines.push('### 关键要点');
    lines.push('');
    keyPoints.forEach((kp, i) => {
      lines.push(`${i + 1}. ${rewriteInternalLinks(kp.trim())}`);
    });
    lines.push('');
  }

  // Insight（钢铁虾的判断）
  if (insight) {
    lines.push('### 我的判断');
    lines.push('');
    lines.push(rewriteInternalLinks(insight).trim());
    lines.push('');
  }

  // Quotes
  if (quotes && quotes.length > 0) {
    lines.push('### 关键引用');
    lines.push('');
    quotes.forEach((q, i) => {
      lines.push(`**${i + 1}.**`);
      if (q.en) lines.push(`> ${q.en}`);
      if (q.zh) lines.push(`> `);
      if (q.zh) lines.push(`> ${q.zh}`);
      lines.push('');
    });
  }

  // 底部
  lines.push('---');
  lines.push('');
  lines.push(`*Saved: ${savedDate || '-'} · Source: aidigest.club*`);
  lines.push('');

  return lines.join('\n');
}

// ---- 主流程 ----

function main() {
  ensureDir(OBSIDIAN_OUT);

  const jsonFiles = fs
    .readdirSync(READS_SRC)
    .filter((f) => f.endsWith('.json'))
    .sort();

  let ok = 0;
  let err = 0;
  const errors = [];

  for (const filename of jsonFiles) {
    const jsonPath = path.join(READS_SRC, filename);
    try {
      const raw = fs.readFileSync(jsonPath, 'utf-8');
      const data = JSON.parse(raw);

      if (!data.slug || !data.titleZh || !data.summaryZh) {
        errors.push(`${filename}: 缺少必需字段 (slug/titleZh/summaryZh)`);
        err++;
        continue;
      }

      const md = convertJsonToMarkdown(data);

      // 文件名：YYYY-MM-DD-slug.md（与 JSON 同名规则）
      const outName = filename.replace(/\.json$/, '.md');
      const outPath = path.join(OBSIDIAN_OUT, outName);
      fs.writeFileSync(outPath, md, 'utf-8');
      ok++;
    } catch (e) {
      errors.push(`${filename}: ${e.message}`);
      err++;
    }
  }

  console.log(`[reads-to-obsidian] 转换完成`);
  console.log(`  ✅ 成功: ${ok}`);
  if (err > 0) {
    console.log(`  ❌ 失败: ${err}`);
    errors.forEach((e) => console.log(`     - ${e}`));
  }
  console.log(`  📂 输出: ${OBSIDIAN_OUT}`);

  if (err > 0) process.exit(1);
}

main();
