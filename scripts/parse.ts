// ⚠️ 已弃用于日报流程 2026-07-12：日报改由 cron 子代理直接写结构化 JSON，不再反解析飞书文档。保留（铁律17）。
// 把飞书 docx raw_content（纯文本）解析成日报结构
import type { DailyReport, Section, NewsItem, SectionKey } from '../src/lib/data';

const SECTION_MAP: Array<{ pattern: RegExp; key: SectionKey; label: string; emoji: string }> = [
  { pattern: /AI\s*热点新闻/i, key: 'news', label: 'AI 热点新闻', emoji: '🔥' },
  { pattern: /企业级\s*AI\s*实践/i, key: 'enterprise', label: '企业级 AI 实践', emoji: '🏢' },
  { pattern: /AI\s*Coding\s*动态/i, key: 'coding', label: 'AI Coding 动态', emoji: '💻' },
  { pattern: /深度报告与论文/i, key: 'report', label: '深度报告与论文', emoji: '📊' },
];

function detectSection(line: string): { key: SectionKey; label: string; emoji: string } | null {
  for (const m of SECTION_MAP) {
    if (m.pattern.test(line)) return { key: m.key, label: m.label, emoji: m.emoji };
  }
  return null;
}

// 是否像「条目标题行」：数字编号 或 emoji + 类目 + | + 标题
// 板块大标题（🔥/🏢/💻/📊 + 板块名）不算，会被 detectSection 单独识别。
function looksLikeItemTitle(line: string): boolean {
  if (/^\*?\*?\s*\d+[.、]\s*\S/.test(line)) return true;
  // emoji 行首 + 有 | / ｜ 分隔符
  if (/^[^\w\u4e00-\u9fa5\d*#>][^|｜\n]*[|｜]\s*.+/u.test(line)) return true;
  return false;
}

// closing（本期速览）段落兜底：命中以下任一则不应进入 closing
// —— 防止新闻条目碎片（来源/启示/链接/条目标题）污染本期速览（参考 6/07 33 段事故）。
function isClosingNoise(line: string): boolean {
  if (/^来源[：:]/.test(line)) return true;
  if (/^启示[：:]/.test(line)) return true;
  if (/https?:\/\//.test(line)) return true;
  if (looksLikeItemTitle(line)) return true;
  return false;
}

// 把「来源：媒体 | https://...」填进 item.source / item.url
function applySource(item: Partial<NewsItem>, rest: string): void {
  const r = rest.trim();
  const parts = r.split(/[|｜]/);
  const src = (parts[0] ?? '').trim();
  if (src && !item.source) item.source = src;
  const urlMatch = r.match(/(https?:\/\/[^\s|｜)）]+)/);
  if (urlMatch && !item.url) item.url = urlMatch[1];
}

// 填 insight（不覆盖已有）
function applyInsight(item: Partial<NewsItem>, rest: string): void {
  const v = rest.trim();
  if (v && !item.insight) item.insight = v;
}

// 从一行里拆出内联的 启示： / 来源： 段，返回 { body, insight, source }
// 格式假设：「<正文> 启示：<启示> 来源：<来源 | url>」，顺序出现、空格分隔。
function splitInlineMeta(line: string): { body?: string; insight?: string; source?: string } {
  const out: { body?: string; insight?: string; source?: string } = {};
  let s = line;
  // 先切 来源：（取最后一个，避免正文里出现“来源”词误切；但带冲号才算）
  const srcIdx = s.search(/\s来源[：:]/);
  if (srcIdx >= 0) {
    out.source = s.slice(srcIdx).replace(/^\s*来源[：:]\s*/, '');
    s = s.slice(0, srcIdx);
  }
  // 再切 启示：
  const insIdx = s.search(/\s启示[：:]/);
  if (insIdx >= 0) {
    out.insight = s.slice(insIdx).replace(/^\s*启示[：:]\s*/, '');
    s = s.slice(0, insIdx);
  }
  const body = s.trim();
  if (body) out.body = body;
  return out;
}

interface RawDayBlock {
  date: string;
  rawTitle?: string;
  lines: string[];
}

// 第 1 步：把全文按 "## YYYY-MM-DD AI 日报" 切分成多天
export function splitByDate(rawContent: string): RawDayBlock[] {
  const lines = rawContent.split(/\r?\n/);
  const days: RawDayBlock[] = [];
  let current: RawDayBlock | null = null;

  // 日界标题正则——必须覆盖文档里所有真实写法，否则当天内容会泄漏进上一天的 daily 文件。
  // 已知写法（2026-06 实测）：
  //   "📅 2026-06-01 AI 日报"        emoji 前缀（最常见，#{0,3} 旧正则因 emoji 非 # 非空白而失配 → 历史污染根因）
  //   "2026-06-05 AI 日报"            纯日期在前
  //   "AI 日报 · 2026-06-12"          日期在后
  //   "修正版：2026-06-15 AI 日报"     带前缀修饰
  // 两个分支：A) 日期在「AI 日报」之前；B) 日期在「AI 日报」之后。
  // 行首允许任意非换行前缀（emoji / # / 中文标点），用 [^\n]*? 非贪婪兜住。
  const dateHeaderBefore = /^[^\n\d]*?(\d{4}-\d{2}-\d{2})[^\n]*?AI\s*日报/;
  const dateHeaderAfter = /^[^\n]*?AI\s*日报[^\n\d]*?(\d{4}-\d{2}-\d{2})/;
  const matchDateHeader = (line: string): string | null => {
    const a = line.match(dateHeaderBefore);
    if (a) return a[1];
    const b = line.match(dateHeaderAfter);
    if (b) return b[1];
    return null;
  };

  for (const line of lines) {
    const matchedDate = matchDateHeader(line);
    if (matchedDate) {
      if (current) days.push(current);
      current = { date: matchedDate, rawTitle: line.replace(/^#+\s*/, '').trim(), lines: [] };
    } else if (current) {
      current.lines.push(line);
    }
  }
  if (current) days.push(current);
  return days;
}

// 第 2 步：把单天内容解析成 sections
export function parseDay(day: RawDayBlock): DailyReport {
  const sections: Section[] = [];
  let currentSection: Section | null = null;
  let currentItem: Partial<NewsItem> | null = null;
  let inClosing = false;
  const closing: string[] = [];
  let summary: string | undefined;

  // 先扫一遍找标题/摘要：很多日报的第 1 段用 ">" 引用块或第一段无前缀长文本作为 summary
  const lines = day.lines.filter((l) => l.trim() !== '');

  function flushItem() {
    if (currentItem && currentSection && currentItem.title && currentItem.body) {
      currentSection.items.push(currentItem as NewsItem);
    }
    currentItem = null;
  }

  function flushSection() {
    flushItem();
    if (currentSection && currentSection.items.length) {
      // 板块去重：同一 key 的 section 合并，不重复 push
      // （防止源文档里「本期小结」后补发的迟到板块产生重复 sections，参考 6/05 6/07 事故）
      const existing = sections.find((s) => s.key === currentSection!.key);
      if (existing) {
        existing.items.push(...currentSection.items);
      } else {
        sections.push(currentSection);
      }
    }
    currentSection = null;
  }

  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line) continue;

    // 跳过分割线、引言行
    if (/^---+$/.test(line)) continue;
    if (/^>/.test(line)) {
      // 引用块，常见于 summary 或元数据
      if (!summary && !currentSection) {
        summary = line.replace(/^>\s*/, '').trim();
      }
      continue;
    }

    // section header (### 🔥 AI 热点新闻 / 🔥 AI 热点新闻 ...)
    const sec = detectSection(line);
    if (sec && /^#{0,3}\s*[🔥🏢💻📊]/u.test(line)) {
      flushSection();
      inClosing = false;
      // 板块去重：若该 key 已存在，续接现有 section 而不新建（迟到板块合并回去）
      const existing = sections.find((s) => s.key === sec.key);
      if (existing) {
        // 从 sections 里取出来当 currentSection，结束时 flushSection 会原地合并
        sections.splice(sections.indexOf(existing), 1);
        currentSection = existing;
      } else {
        currentSection = { ...sec, items: [] };
      }
      continue;
    }

    // closing block
    if (/^#{0,3}\s*📝\s*本期小结/.test(line)) {
      flushSection();
      inClosing = true;
      continue;
    }

    if (inClosing) {
      // 遇到条目标题行（后补的迟到新闻）→ 复位，让后续逻辑当作正常条目处理
      // （参考 6/07 33 段污染：「本期小结」后又出现 emoji 条目标题，不能全吞进 closing）
      if (looksLikeItemTitle(line) && currentSection) {
        inClosing = false;
        // 不 continue，落到下面的条目标题识别逻辑
      } else {
        // 只把「真正的速览段落」堆进 closing：足够长、不是来源/启示/链接/条目标题
        if (line.length > 20 && !/^#/.test(line) && !isClosingNoise(line)) {
          closing.push(line.replace(/^\*\*[^*]+\*\*\s*/, '').trim());
        }
        continue;
      }
    }

    if (!currentSection) continue;

    // 条目标题识别 —— 支持两种格式：
    //   1) 数字编号：**1. 标题** / **1、标题** / 1. 标题 / 1、标题
    //   2) Emoji + 类目前缀：💰 融资 | 标题 / 🚀 产品发布 | 标题 / 📜 监管政策 | 标题 等
    //   注意：板块大标题（🔥/🏢/💻/📊 + 板块名）已在前面被 detectSection 拦截，到这里的 emoji 行都是条目标题
    const itemTitleMatch = line.match(/^\*?\*?\s*(\d+)[.、]\s*\*?\*?\s*(.+?)\*?\*?$/);
    // emoji item header: 任意 emoji（含变体选择符）+ 可选类目 + | + 标题
    // 简化：行首可有可选的 ** / * 粗体包裹，随后是 emoji（非中英文/数字/井号/引用符），后面跟有 " | " 或 "｜" 分隔的标题
    // 注意：允许前导 * 是为兼容飞书往返后条目标题带 **...** 粗体包裹的写法（2026-07-06 修复：此前前导 * 被排除导致整条目丢失）
    const emojiItemMatch = !itemTitleMatch && /^\*{0,2}\s*[^\w\u4e00-\u9fa5\d*#>][^|｜\n]*[|｜]\s*.+/u.test(line)
      ? line.match(/^\*{0,2}\s*([^\w\u4e00-\u9fa5\d*#>][^|｜]*?)[|｜]\s*(.+?)\*?\*?$/u)
      : null;
    if (itemTitleMatch && /[\u4e00-\u9fa5\w]/.test(itemTitleMatch[2])) {
      flushItem();
      // 清掉前后的 ** 包裹
      const title = itemTitleMatch[2].replace(/^\*\*/, '').replace(/\*\*$/, '').trim();
      currentItem = { title };
      continue;
    }
    if (emojiItemMatch && /[\u4e00-\u9fa5\w]/.test(emojiItemMatch[2])) {
      flushItem();
      const category = emojiItemMatch[1].trim().replace(/\*+/g, '').trim();
      const title = emojiItemMatch[2].replace(/^\*\*/, '').replace(/\*\*$/, '').trim();
      // 把类目作为前缀放到 title 里（如 "💰 融资 | Google 加码 400 亿"），保持原文本可读性
      currentItem = { title: category ? `${category} | ${title}` : title };
      continue;
    }

    if (!currentItem) continue;

    // 启示（整行）
    if (/^启示[：:]/.test(line)) {
      applyInsight(currentItem, line.replace(/^启示[：:]\s*/, ''));
      continue;
    }

    // 来源 + 链接（整行）
    if (/^来源[：:]/.test(line)) {
      applySource(currentItem, line.replace(/^来源[：:]\s*/, ''));
      continue;
    }

    // 关键修复：很多日报把「正文 + 启示：… + 来源：…」写在同一物理行（空格分隔），
    // 旧逻辑只认行首 ^启示/^来源，导致 insight/source/url 全丢、整段堆进 body。
    // 这里把内联的 启示：/来源： 段切出来，正文部分继续走 body 累加。
    {
      const inline = splitInlineMeta(line);
      if (inline.insight) applyInsight(currentItem, inline.insight);
      if (inline.source) applySource(currentItem, inline.source);
      if (inline.body) {
        if (currentItem.body) currentItem.body = `${currentItem.body} ${inline.body}`;
        else currentItem.body = inline.body;
      }
      continue;
    }

    // 否则当作 body 累加（理论上到不了这里，保留兜底）
    if (currentItem.body) {
      currentItem.body = `${currentItem.body} ${line}`;
    } else {
      currentItem.body = line;
    }
  }
  flushSection();

  return {
    date: day.date,
    title: day.rawTitle?.replace(/AI\s*日报.*$/, '').trim() || `${day.date} AI 日报`,
    summary,
    sections,
    closing: closing.length ? closing : undefined,
  };
}

// 日期去重 / 合并：源文档可能出现同一天多个「## YYYY-MM-DD AI 日报」标题块
// （参考 6/07：L495 / L525 两个 2026-06-07 标题）——同日多块合并为一，避免后者覆盖前者
function mergeDuplicateDates(reports: DailyReport[]): DailyReport[] {
  const byDate = new Map<string, DailyReport>();
  for (const r of reports) {
    const existing = byDate.get(r.date);
    if (!existing) {
      byDate.set(r.date, r);
      continue;
    }
    // 合并 sections（按 key）
    for (const s of r.sections) {
      const es = existing.sections.find((x) => x.key === s.key);
      if (es) es.items.push(...s.items);
      else existing.sections.push(s);
    }
    // 合并 closing（去重）
    if (r.closing && r.closing.length) {
      const set = new Set(existing.closing ?? []);
      const merged = [...(existing.closing ?? [])];
      for (const c of r.closing) if (!set.has(c)) { set.add(c); merged.push(c); }
      existing.closing = merged;
    }
    if (!existing.summary && r.summary) existing.summary = r.summary;
  }
  return [...byDate.values()];
}

// item 去重（按 title）：同一 section 合并后可能出现重复条目
function dedupeItems(report: DailyReport): DailyReport {
  for (const s of report.sections) {
    const seen = new Set<string>();
    s.items = s.items.filter((it) => {
      const k = (it.title ?? '').trim();
      if (!k || seen.has(k)) return false;
      seen.add(k);
      return true;
    });
  }
  return report;
}

// 入口：raw text -> reports[]
export function parseAll(rawContent: string): DailyReport[] {
  const parsed = splitByDate(rawContent).map(parseDay);
  const merged = mergeDuplicateDates(parsed).map(dedupeItems);
  return merged.filter((r) => r.sections.length > 0);
}
