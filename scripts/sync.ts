// 主同步流程：飞书文档 → 解析 → 清洗 → 写 src/data/daily/*.json
import 'dotenv/config';
import fs from 'node:fs';
import path from 'node:path';
import { getTenantToken, getDocxRaw } from './feishu';
import { parseAll } from './parse';
import { sanitizeReport } from './sanitize';

const ROOT = path.resolve(process.cwd());
const DATA_DIR = path.join(ROOT, 'src/data/daily');

interface RunOptions {
  dryRun?: boolean;     // 不写文件
  noLLM?: boolean;      // 关闭 LLM 清洗（仅离线兜底）
  onlyDate?: string;    // 只同步指定一天
}

async function main() {
  const args = process.argv.slice(2);
  const opts: RunOptions = {
    dryRun: args.includes('--dry-run'),
    noLLM: args.includes('--no-llm'),
    onlyDate: args.find((a) => /^--date=/.test(a))?.replace('--date=', ''),
  };

  const appId = required('FEISHU_APP_ID');
  const appSecret = required('FEISHU_APP_SECRET');
  const docToken = required('DOC_TOKEN');

  const llmCfg = opts.noLLM
    ? null
    : process.env.LLM_API_KEY
    ? {
        apiBase: process.env.LLM_API_BASE ?? 'https://api.openai.com/v1',
        apiKey: process.env.LLM_API_KEY,
        model: process.env.LLM_MODEL ?? 'gpt-4o-mini',
        protocol: (process.env.LLM_PROTOCOL ?? 'openai') as 'openai' | 'anthropic',
      }
    : null;

  if (!llmCfg) {
    console.warn('[sync] No LLM_API_KEY: sensitive content will use offline keyword replacement only.');
  }

  console.log('[sync] Fetching token...');
  const token = await getTenantToken(appId, appSecret);

  console.log(`[sync] Fetching docx ${docToken}...`);
  const raw = await getDocxRaw(docToken, token);
  console.log(`[sync] Got ${raw.length} chars`);

  const reports = parseAll(raw);
  console.log(`[sync] Parsed ${reports.length} day(s): ${reports.map((r) => r.date).join(', ')}`);

  const filtered = opts.onlyDate ? reports.filter((r) => r.date === opts.onlyDate) : reports;

  if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

  for (const report of filtered) {
    console.log(`[sync] Sanitizing ${report.date}...`);
    const cleaned = await sanitizeReport(report, llmCfg);
    const out = path.join(DATA_DIR, `${cleaned.date}.json`);
    if (opts.dryRun) {
      console.log(`[sync] [dry-run] would write ${out}`);
      console.log(JSON.stringify(cleaned, null, 2).slice(0, 600), '...');
    } else {
      fs.writeFileSync(out, JSON.stringify(cleaned, null, 2) + '\n', 'utf-8');
      console.log(`[sync] wrote ${out} (${cleaned.sections.length} sections, ${countItems(cleaned)} items)`);
    }
  }

  console.log('[sync] Done.');
}

function required(name: string): string {
  const v = process.env[name];
  if (!v) {
    console.error(`Missing env: ${name}`);
    process.exit(1);
  }
  return v;
}

function countItems(r: { sections: { items: unknown[] }[] }): number {
  return r.sections.reduce((sum, s) => sum + s.items.length, 0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
