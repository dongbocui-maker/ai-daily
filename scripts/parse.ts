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

  const dateHeader = /^#{0,3}\s*(\d{4}-\d{2}-\d{2})\s*AI\s*日报/;

  for (const line of lines) {
    const m = line.match(dateHeader);
    if (m) {
      if (current) days.push(current);
      current = { date: m[1], rawTitle: line.replace(/^#+\s*/, '').trim(), lines: [] };
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
      sections.push(currentSection);
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
      currentSection = { ...sec, items: [] };
      continue;
    }

    // closing block
    if (/^#{0,3}\s*📝\s*本期小结/.test(line)) {
      flushSection();
      inClosing = true;
      continue;
    }

    if (inClosing) {
      // 把段落原文堆进 closing
      if (line.length > 20 && !/^#/.test(line)) {
        closing.push(line.replace(/^\*\*[^*]+\*\*\s*/, '').trim());
      }
      continue;
    }

    if (!currentSection) continue;

    // 条目标题识别 —— 支持两种格式：
    //   1) 数字编号：**1. 标题** / **1、标题** / 1. 标题 / 1、标题
    //   2) Emoji + 类目前缀：💰 融资 | 标题 / 🚀 产品发布 | 标题 / 📜 监管政策 | 标题 等
    //   注意：板块大标题（🔥/🏢/💻/📊 + 板块名）已在前面被 detectSection 拦截，到这里的 emoji 行都是条目标题
    const itemTitleMatch = line.match(/^\*?\*?\s*(\d+)[.、]\s*\*?\*?\s*(.+?)\*?\*?$/);
    // emoji item header: 任意 emoji（含变体选择符）+ 可选类目 + | + 标题
    // 简化：行首是 emoji（非中英文/数字/星号字符），后面跟有 " | " 或 "｜" 分隔的标题
    const emojiItemMatch = !itemTitleMatch && /^[^\w\u4e00-\u9fa5\d*#>][^|｜\n]*[|｜]\s*.+/u.test(line)
      ? line.match(/^([^\w\u4e00-\u9fa5\d*#>][^|｜]*?)[|｜]\s*(.+?)\*?\*?$/u)
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

    // 启示
    if (/^启示[：:]/.test(line)) {
      currentItem.insight = line.replace(/^启示[：:]\s*/, '').trim();
      continue;
    }

    // 来源 + 链接
    if (/^来源[：:]/.test(line)) {
      const rest = line.replace(/^来源[：:]\s*/, '');
      // 期望格式 "来源：媒体名 | https://..."
      const parts = rest.split(/[|｜]/);
      currentItem.source = (parts[0] ?? '').trim();
      const urlMatch = rest.match(/(https?:\/\/[^\s|｜)）]+)/);
      if (urlMatch) currentItem.url = urlMatch[1];
      continue;
    }

    // 否则当作 body 累加
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

// 入口：raw text -> reports[]
export function parseAll(rawContent: string): DailyReport[] {
  return splitByDate(rawContent).map(parseDay).filter((r) => r.sections.length > 0);
}
