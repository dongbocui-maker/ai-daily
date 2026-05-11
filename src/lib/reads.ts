// 加载「精读」JSON 数据 —— 使用 Vite 的 glob 导入

export interface ReadQuote {
  en?: string;
  zh: string;
}

/** 音频元数据（跳 Hero 区下方渲染播放器） */
export interface ReadAudio {
  url: string;                 // COS 公网 URL
  duration_seconds: number;    // ffprobe 探测的精确时长
  size_bytes: number;          // 文件大小
  generated_at: string;        // ISO 时间戳
  format?: 'mp3' | 'm4a';      // 默认 m4a（NotebookLM 输出）
  // 后期可加：transcript / subtitle_url
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
  audio?: ReadAudio;        // 可选：NotebookLM 生成的双人对谈播客
  /** 可选：精读概要 PPT（PDF 形式，浏览器可直接预览）
   *  路径建议：/decks/<slug>.pdf （public 下）
   */
  deckPdfUrl?: string;
  /** 可选：原始 .pptx 文件（供下载/编辑） */
  deckPptxUrl?: string;
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
