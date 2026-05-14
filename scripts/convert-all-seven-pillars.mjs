// Batch convert /tmp/blocks/*.json -> src/content/seven-pillars/*.md
// Preserves frontmatter from existing files
import { execFileSync } from 'child_process';
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import path from 'path';

const DOCS = [
  { order: 0,  slug: 'introduction',         docNum: '00 · 引言',         docColor: 'foundation', title: '研究背景与方法论',     token: 'YBYqdU0gnouVsqxOjf6cMIHPnpX' },
  { order: 1,  slug: 'foundation-overview',  docNum: '01 · 底座 · 概览',   docColor: 'foundation', title: '为什么是「一个底座+七柱」', token: 'PyN0dgI4BoUFMfxE8Hqc7rEmnzc' },
  { order: 2,  slug: 'foundation-data',      docNum: '02 · 底座 · 数据',   docColor: 'foundation', title: '数据治理 + 知识管理',    token: 'SryAdUFhaoeGusxUL4NcwAftnTc' },
  { order: 3,  slug: 'architecture',         docNum: '03 · 柱 1',          docColor: 'p1',         title: 'Agentic 架构与 Mesh', token: 'Lr8Fd9uHlofhhuxLwipc9eTVn2b' },
  { order: 4,  slug: 'api-governance',       docNum: '04 · 柱 2',          docColor: 'p2',         title: 'API 治理与 Gateway',  token: 'UZaHd6hz3okGHrxAzfBcW3vqndh' },
  { order: 5,  slug: 'llmops',               docNum: '05 · 柱 3',          docColor: 'p3',         title: 'LLMOps / AgentOps',   token: 'T9PJd9NsCo1M0UxN3zhcS91gnNe' },
  { order: 6,  slug: 'risk-iam',             docNum: '06 · 柱 4',          docColor: 'p4',         title: '风险治理 + IAM',       token: 'ShovdCMBxokvmXxWl3NcOrUsnnf' },
  { order: 7,  slug: 'talent-org',           docNum: '07 · 柱 5',          docColor: 'p5',         title: '人才与组织设计',        token: 'VmGwdIQBvoyLQhxGl91cCgLunEm' },
  { order: 8,  slug: 'change-mgmt',          docNum: '08 · 柱 6',          docColor: 'p6',         title: '变革管理',             token: 'GPLsdlnW7oI3YfxhI2LccTo1nGg' },
  { order: 9,  slug: 'finops-roi',           docNum: '09 · 柱 7',          docColor: 'p7',         title: 'FinOps / ROI',        token: 'FHOjdlctWoiVeWxWq8QcH1AOnqd' },
  { order: 10, slug: 'conclusion',           docNum: '10 · 总结',          docColor: 'conclusion', title: '协同矩阵+成熟度评估+路线图', token: 'IIJAdnWVNofjqwxsA9Ucu6uenAg' },
];

// Parse existing frontmatter to keep words field if present
function readExistingFrontmatter(fp) {
  try {
    const raw = readFileSync(fp, 'utf-8');
    if (!raw.startsWith('---')) return {};
    const end = raw.indexOf('\n---', 4);
    if (end < 0) return {};
    const fm = raw.slice(4, end);
    const out = {};
    for (const line of fm.split('\n')) {
      const m = line.match(/^([a-zA-Z_]+):\s*(.+)$/);
      if (!m) continue;
      let v = m[2].trim();
      if (v.startsWith('"') && v.endsWith('"')) v = v.slice(1, -1);
      out[m[1]] = v;
    }
    return out;
  } catch { return {}; }
}

const OUT_DIR = path.resolve('src/content/seven-pillars');
const BLOCKS_DIR = path.resolve('/tmp/blocks');
const CONVERTER = path.resolve('scripts/feishu-blocks-to-markdown.mjs');

let total = 0;
for (const d of DOCS) {
  const orderStr = String(d.order).padStart(2, '0');
  const inFile = path.join(BLOCKS_DIR, `${orderStr}-${d.slug}.json`);
  const outFile = path.join(OUT_DIR, `${orderStr}-${d.slug}.md`);
  const existing = readExistingFrontmatter(outFile);

  let md;
  try {
    md = execFileSync('node', [CONVERTER, inFile], { encoding: 'utf-8' });
  } catch (e) {
    console.error(`[FAIL] ${d.slug}: ${e.message}`);
    process.exit(1);
  }

  const fmLines = [
    '---',
    `order: ${d.order}`,
    `slug: ${d.slug}`,
    `docNum: "${d.docNum}"`,
    `docColor: ${d.docColor}`,
    `title: "${d.title}"`,
    `feishuToken: ${d.token}`,
  ];
  if (existing.words) fmLines.push(`words: "${existing.words}"`);
  fmLines.push('---', '');
  const final = fmLines.join('\n') + md;
  writeFileSync(outFile, final);
  const newSize = statSync(outFile).size;
  console.log(`[ok] ${orderStr}-${d.slug}.md  ${newSize} bytes`);
  total++;
}
console.log(`Total: ${total} files written`);
