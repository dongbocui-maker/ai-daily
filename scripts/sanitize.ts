// LLM 清洗：去客户名、去内部 MD/咨询视角、保留新闻本体 + 通用行业洞察
import type { DailyReport, NewsItem } from '../src/lib/data';

// 关键词黑名单：命中即触发改写（regex / 包含匹配）
const SENSITIVE_PATTERNS: RegExp[] = [
  /L['']?Or[ée]al/i,
  /欧莱雅/,
  /LVMH/i,
  /路易威登/,
  /埃森哲/,
  /Accenture/i,
  /\bMD\s*层面/,
  /我们应该/,
  /我们公司/,
  /客户.*L|LVMH/,
];

const TITLE = '你是一名英中双语 AI 行业资讯编辑。';

const PROMPT = `${TITLE}

任务：把下面这条新闻条目改写成"中性的行业资讯版本"，用于公开的科技博客发布。

改写规则：
1. 必须删除所有特定企业客户名（如 L'Oréal / LVMH / 欧莱雅 / 路易威登），改用"快消客户/奢侈品客户/头部 B2C 品牌"等通用表述。
2. 必须删除咨询公司或内部视角措辞（如"埃森哲应该…"、"我们应该…"、"MD 层面需要…"、"咨询方需要…"），改写为面向"企业 / 行业 / CIO / 决策者"的中性洞察。
3. 不改变核心事实（公司名、产品名、数字、时间、链接）。
4. 不改变板块定位（这条原本属于"AI 热点新闻"就保持新闻视角）。
5. 中文行文，不超过原文长度。
6. 输出严格 JSON，字段：title / body / insight。其它字段不要改、不要返回。

原条目：
\`\`\`json
{INPUT}
\`\`\`

只输出修订后的 JSON，不要解释、不要 markdown 代码块包裹。`;

function needsRewrite(item: NewsItem): boolean {
  const blob = `${item.title}\n${item.body}\n${item.insight ?? ''}`;
  return SENSITIVE_PATTERNS.some((p) => p.test(blob));
}

interface LLMConfig {
  apiBase: string;
  apiKey: string;
  model: string;
  protocol?: 'openai' | 'anthropic';
}

async function callLLM(cfg: LLMConfig, prompt: string): Promise<string> {
  const protocol = cfg.protocol ?? 'openai';
  if (protocol === 'anthropic') {
    return callAnthropicLLM(cfg, prompt);
  }
  return callOpenAILLM(cfg, prompt);
}

async function callOpenAILLM(cfg: LLMConfig, prompt: string): Promise<string> {
  const res = await fetch(`${cfg.apiBase.replace(/\/$/, '')}/chat/completions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${cfg.apiKey}`,
    },
    body: JSON.stringify({
      model: cfg.model,
      temperature: 0.2,
      messages: [
        { role: 'system', content: TITLE },
        { role: 'user', content: prompt },
      ],
      response_format: { type: 'json_object' },
    }),
  });
  if (!res.ok) throw new Error(`LLM call failed ${res.status}: ${await res.text()}`);
  const json = (await res.json()) as { choices: Array<{ message: { content: string } }> };
  return json.choices[0].message.content;
}

async function callAnthropicLLM(cfg: LLMConfig, prompt: string): Promise<string> {
  // Anthropic Messages API（Azure 也是这个 schema）
  const res = await fetch(`${cfg.apiBase.replace(/\/$/, '')}/messages`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': cfg.apiKey,
      'anthropic-version': '2023-06-01',
      Authorization: `Bearer ${cfg.apiKey}`, // Azure 兼容
    },
    body: JSON.stringify({
      model: cfg.model,
      max_tokens: 2000,
      // 注：Claude Opus 4.7 不再接受 temperature 参数
      system: TITLE + '\n\n严格输出 JSON 对象（不带任何前后说明、不带 markdown 代码块包裹）。',
      messages: [{ role: 'user', content: prompt }],
    }),
  });
  if (!res.ok) throw new Error(`LLM call failed ${res.status}: ${await res.text()}`);
  const json = (await res.json()) as { content: Array<{ type: string; text?: string }> };
  const block = json.content?.find((b) => b.type === 'text') ?? json.content?.[0];
  const raw = (block?.text ?? '').trim();
  // 兼容模型偶尔包 ```json ... ``` 的情况
  return raw.replace(/^```(?:json)?\s*/i, '').replace(/```\s*$/i, '').trim();
}

export async function sanitizeReport(report: DailyReport, cfg: LLMConfig | null): Promise<DailyReport> {
  // closing 段也清洗
  const newSections = await Promise.all(
    report.sections.map(async (sec) => ({
      ...sec,
      items: await Promise.all(
        sec.items.map(async (item) => {
          if (!needsRewrite(item)) return item;
          if (!cfg) {
            // 离线兜底：硬替换关键词
            return offlineSanitize(item);
          }
          try {
            const out = await callLLM(cfg, PROMPT.replace('{INPUT}', JSON.stringify(item, null, 2)));
            const parsed = JSON.parse(out) as Partial<NewsItem>;
            return {
              ...item,
              title: parsed.title ?? item.title,
              body: parsed.body ?? item.body,
              insight: parsed.insight ?? item.insight,
            };
          } catch (err) {
            console.warn(`[sanitize] LLM failed for "${item.title}", fallback to offline`, err);
            return offlineSanitize(item);
          }
        }),
      ),
    })),
  );
  return { ...report, sections: newSections };
}

function offlineSanitize(item: NewsItem): NewsItem {
  // 通用兜底替换，按从特定到泛化的顺序
  const replace = (s?: string) =>
    s
      // 客户名（注意：先处理含品牌组合的，再处理简称）
      ?.replace(/L['']?Or[ée]al|欧莱雅/gi, '某快消客户')
      ?.replace(/LVMH|路易威登|Louis\s*Vuitton|Dior|Chanel/gi, '某奢侈品客户')
      // 公司名
      ?.replace(/埃森哲|Accenture/gi, '咨询行业')
      // 内部视角：仅换明显“从咨询公司身份说话”的陈述
      // 不动作为中性职位描述的 MD/CIO（那些是面向企业读者的中性表述）
      ?.replace(/\bMD\s*层面需[^，。；！]{0,8}/g, '决策者层面需')
      ?.replace(/合伙人层面需/g, '决策者需')
      ?.replace(/咨询(?:方|公司|顾问)(?:需(?:要|在)?|应)/g, '行业服务商应')
      // “我们”：仅在上下文明显是咨询者口吻时才换（避免误伤引述原文，如 OpenAI “我们的原则”）
      ?.replace(/我们应(?:该|当)把/g, '企业应把')
      ?.replace(/我们需要(?:帮|为)客户/g, '服务商需为客户')
      ?.replace(/我们公司/g, '相关企业')
      // 客户视角混入
      ?.replace(/对(?:我方|我们)客户/g, '对企业客户');
  return {
    ...item,
    title: replace(item.title) ?? item.title,
    body: replace(item.body) ?? item.body,
    insight: replace(item.insight),
  };
}
