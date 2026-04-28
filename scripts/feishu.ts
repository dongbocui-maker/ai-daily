// 飞书 API 客户端 —— 拉取 docx 文档纯文本与 block 树
const FEISHU_BASE = 'https://open.feishu.cn/open-apis';

let cachedToken: { token: string; expireAt: number } | null = null;

export async function getTenantToken(appId: string, appSecret: string): Promise<string> {
  if (cachedToken && cachedToken.expireAt > Date.now() + 60_000) {
    return cachedToken.token;
  }
  const res = await fetch(`${FEISHU_BASE}/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
  });
  const json = (await res.json()) as { code: number; msg?: string; tenant_access_token: string; expire: number };
  if (json.code !== 0) throw new Error(`Feishu auth failed: ${json.code} ${json.msg}`);
  cachedToken = {
    token: json.tenant_access_token,
    expireAt: Date.now() + json.expire * 1000,
  };
  return cachedToken.token;
}

export async function getDocxRaw(docToken: string, token: string): Promise<string> {
  const res = await fetch(`${FEISHU_BASE}/docx/v1/documents/${docToken}/raw_content?lang=0`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  const json = (await res.json()) as { code: number; msg?: string; data?: { content: string } };
  if (json.code !== 0) throw new Error(`Feishu raw_content failed: ${json.code} ${json.msg}`);
  return json.data?.content ?? '';
}

interface BlockChildren {
  blocks: Array<{
    block_id: string;
    block_type: number;
    parent_id: string;
    children?: string[];
    [key: string]: unknown;
  }>;
  has_more: boolean;
  page_token?: string;
}

export async function listAllBlocks(docToken: string, token: string) {
  const all: BlockChildren['blocks'] = [];
  let pageToken: string | undefined;
  do {
    const url = new URL(`${FEISHU_BASE}/docx/v1/documents/${docToken}/blocks`);
    url.searchParams.set('page_size', '500');
    url.searchParams.set('document_revision_id', '-1');
    if (pageToken) url.searchParams.set('page_token', pageToken);
    const res = await fetch(url, { headers: { Authorization: `Bearer ${token}` } });
    const json = (await res.json()) as { code: number; msg?: string; data?: { items: BlockChildren['blocks']; has_more: boolean; page_token?: string } };
    if (json.code !== 0) throw new Error(`Feishu list blocks failed: ${json.code} ${json.msg}`);
    all.push(...(json.data?.items ?? []));
    pageToken = json.data?.has_more ? json.data?.page_token : undefined;
  } while (pageToken);
  return all;
}
