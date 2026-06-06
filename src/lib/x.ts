export type XKind = 'x' | 'podcast' | 'blog';

export interface XSignalItem {
  id: string;
  kind: XKind;
  source: string;
  sourceName: string;
  handle?: string;
  title: string;
  summaryEn: string;
  insightZh: string;
  tags?: string[];
  url?: string;
  publishedAt?: string | null;
  author?: string;
  metrics?: {
    likes?: number;
    retweets?: number;
    replies?: number;
    score?: number;
  };
}

export interface XSignalSection {
  key: XKind;
  label: string;
  description?: string;
  items: XSignalItem[];
}

export interface XDailyData {
  date: string;
  title: string;
  generatedAt: string;
  feedGeneratedAt?: string | null;
  summary: string;
  stats: {
    xBuilders: number;
    totalTweets: number;
    podcastEpisodes: number;
    blogPosts: number;
    selectedItems: number;
  };
  featured?: XSignalItem[];
  sections: XSignalSection[];
  errors?: string[];
  audit?: Record<string, unknown>;
}

const modules = import.meta.glob<XDailyData>('../data/x/daily/*.json', {
  eager: true,
  import: 'default',
});

const reports: Record<string, XDailyData> = {};
for (const [filePath, mod] of Object.entries(modules)) {
  const m = filePath.match(/([0-9]{4}-[0-9]{2}-[0-9]{2})\.json$/);
  if (m) reports[m[1]] = mod as XDailyData;
}

export function listXDates(): string[] {
  return Object.keys(reports).sort().reverse();
}

export function loadLatestX(): XDailyData | null {
  const dates = listXDates();
  return dates[0] ? reports[dates[0]] : null;
}

export function loadXDate(date: string): XDailyData | null {
  return reports[date] ?? null;
}

export function allXItems(report: XDailyData): XSignalItem[] {
  return report.sections.flatMap((section) => section.items.map((item) => ({ ...item, kind: section.key })));
}
