// Fetch all 11 七柱 docs as block JSON to /tmp/blocks/<order>-<slug>.json
import 'dotenv/config';
import fs from 'node:fs';
import path from 'node:path';
import { getTenantToken, listAllBlocks } from './feishu';

const DOCS = [
  { order: '00', slug: 'introduction',         token: 'YBYqdU0gnouVsqxOjf6cMIHPnpX' },
  { order: '01', slug: 'foundation-overview',  token: 'PyN0dgI4BoUFMfxE8Hqc7rEmnzc' },
  { order: '02', slug: 'foundation-data',      token: 'SryAdUFhaoeGusxUL4NcwAftnTc' },
  { order: '03', slug: 'architecture',         token: 'Lr8Fd9uHlofhhuxLwipc9eTVn2b' },
  { order: '04', slug: 'api-governance',       token: 'UZaHd6hz3okGHrxAzfBcW3vqndh' },
  { order: '05', slug: 'llmops',               token: 'T9PJd9NsCo1M0UxN3zhcS91gnNe' },
  { order: '06', slug: 'risk-iam',             token: 'ShovdCMBxokvmXxWl3NcOrUsnnf' },
  { order: '07', slug: 'talent-org',           token: 'VmGwdIQBvoyLQhxGl91cCgLunEm' },
  { order: '08', slug: 'change-mgmt',          token: 'GPLsdlnW7oI3YfxhI2LccTo1nGg' },
  { order: '09', slug: 'finops-roi',           token: 'FHOjdlctWoiVeWxWq8QcH1AOnqd' },
  { order: '10', slug: 'conclusion',           token: 'IIJAdnWVNofjqwxsA9Ucu6uenAg' },
];

async function main() {
  const appId = process.env.FEISHU_APP_ID!;
  const appSecret = process.env.FEISHU_APP_SECRET!;
  if (!appId || !appSecret) throw new Error('Missing FEISHU_APP_ID/SECRET');
  const outDir = process.argv[2] || '/tmp/blocks';
  fs.mkdirSync(outDir, { recursive: true });

  const onlyOrder = process.argv[3]; // optional: '00' to fetch single
  console.log('[fetch] Getting tenant token...');
  const token = await getTenantToken(appId, appSecret);
  console.log('[fetch] Token OK');

  for (const d of DOCS) {
    if (onlyOrder && d.order !== onlyOrder) continue;
    process.stdout.write(`[fetch] ${d.order} ${d.slug} ${d.token} ... `);
    const blocks = await listAllBlocks(d.token, token);
    const fp = path.join(outDir, `${d.order}-${d.slug}.json`);
    fs.writeFileSync(fp, JSON.stringify({ blocks }, null, 2));
    console.log(`${blocks.length} blocks, ${fs.statSync(fp).size} bytes`);
    if (blocks.length < 30) {
      console.warn(`[WARN] ${d.slug} only got ${blocks.length} blocks — may be incomplete`);
    }
    // Rate limit polite
    await new Promise(r => setTimeout(r, 200));
  }
  console.log('[fetch] done');
}

main().catch(e => { console.error(e); process.exit(1); });
