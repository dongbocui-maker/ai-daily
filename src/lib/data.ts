// 加载日报 JSON 数据 —— 使用 Vite 的 glob 导入
export type SectionKey = 'news' | 'enterprise' | 'coding' | 'report';

export interface NewsItem {
  title: string;
  body: string;
  insight?: string;
  source?: string;
  url?: string;
}

export interface Section {
  key: SectionKey;
  label: string;
  emoji: string;
  items: NewsItem[];
}

export interface DailyReport {
  date: string;
  title: string;
  summary?: string;
  sections: Section[];
  closing?: string[];
}

// Vite glob: 静态构建期把所有 JSON 内嵌
const modules = import.meta.glob<DailyReport>('../data/daily/*.json', {
  eager: true,
  import: 'default',
});

// 构建 date -> report 映射
const reports: Record<string, DailyReport> = {};
for (const [filePath, mod] of Object.entries(modules)) {
  const m = filePath.match(/([0-9]{4}-[0-9]{2}-[0-9]{2})\.json$/);
  if (m) reports[m[1]] = mod as DailyReport;
}

export function listDates(): string[] {
  return Object.keys(reports).sort().reverse();
}

export function loadDate(date: string): DailyReport | null {
  return reports[date] ?? null;
}

export function loadAll(): DailyReport[] {
  return listDates().map((d) => reports[d]);
}

export function loadLatest(): DailyReport | null {
  const dates = listDates();
  return dates[0] ? reports[dates[0]] : null;
}

export function formatDateZh(date: string): string {
  const [y, m, d] = date.split('-').map(Number);
  return `${y} 年 ${m} 月 ${d} 日`;
}

export function formatDateShort(date: string): string {
  const [, m, d] = date.split('-').map(Number);
  return `${m}.${d.toString().padStart(2, '0')}`;
}

export function dayOfWeekZh(date: string): string {
  const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
  return days[new Date(date).getDay()];
}
