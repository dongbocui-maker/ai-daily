// 加载「精读」JSON 数据 —— 使用 Vite 的 glob 导入

export interface ReadQuote {
  en?: string;
  zh: string;
}

export interface ReadArticle {
  slug: string;
  savedDate: string;        // 你收藏日期 YYYY-MM-DD
  publishDate?: string;     // 原文发布日期 YYYY-MM-DD
  titleZh: string;          // 中文标题
  titleEn?: string;         // 原标题（英文）
  author: string;
  authorTitle?: string;     // 作者头衔
  originalUrl: string;
  tags: string[];
  summary: string;          // 一句话核心观点（30-50 字）
  keyPoints: string[];      // 核心观点（3-5 条）
  insight?: string;         // 启示与思考（钢铁虾视角）
  summaryZh: string;        // 完整中文解读（markdown）
  quotes?: ReadQuote[];     // 金句精选
  source: 'manual' | 'auto'; // 手工添加 vs cron 自动收集
}

// Vite glob: 静态构建期把所有 JSON 内嵌
const modules = import.meta.glob<ReadArticle>('../data/reads/*.json', {
  eager: true,
  import: 'default',
});

const articles: Record<string, ReadArticle> = {};
for (const [filePath, mod] of Object.entries(modules)) {
  const m = filePath.match(/([^/]+)\.json$/);
  if (m) {
    const data = mod as ReadArticle;
    articles[data.slug] = data;
  }
}

export function listReads(): ReadArticle[] {
  // 按 savedDate 倒序
  return Object.values(articles).sort((a, b) =>
    b.savedDate.localeCompare(a.savedDate)
  );
}

export function loadRead(slug: string): ReadArticle | null {
  return articles[slug] ?? null;
}

export function listSlugs(): string[] {
  return Object.keys(articles);
}
