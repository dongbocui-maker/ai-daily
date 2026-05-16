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

export interface AudioMeta {
  url: string;                 // COS 公网 URL
  duration_seconds: number;    // ffprobe 探测的精确时长
  size_bytes: number;          // 文件大小
  generated_at: string;        // ISO 时间戳
  // 后期可加：transcript / subtitle_url（字幕功能时）
}

// 审计/元数据字段——仅供内部追溯，**不渲染到前端用户界面**
export interface AuditMeta {
  tieluFourScan?: string;     // 铁律 4 扫描结果声明（OpenAI/Anthropic/Google DeepMind/Meta/Microsoft 大动作扫描）
  [key: string]: unknown;     // 未来其他审计字段
}

export interface DailyReport {
  date: string;
  title: string;
  summary?: string;
  sections: Section[];
  // 本期速览（Brief）面向读者的核心趋势总结，通常 2-3 段。
  // ⚠️ 不要往里塞「铁律 X 扫描结果」「审计日志」之类的内部元信息——那是 audit 字段的事。
  closing?: string[];
  audio?: AudioMeta;          // 可选：当天日报的语音版 mp3
  audit?: AuditMeta;          // 可选：内部审计元数据，不渲染
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

/** 取当月代号 YYYY-MM（如 "2026-04"） */
export function getYearMonth(date: string): string {
  return date.slice(0, 7);
}

/** 返回"当月"的日期列表（以最新一天为参考） */
export function listCurrentMonthDates(): string[] {
  const all = listDates();
  if (!all.length) return [];
  const currentMonth = getYearMonth(all[0]);
  return all.filter((d) => getYearMonth(d) === currentMonth);
}

/** 返回当月说明（如 "2026 年 4 月"） */
export function currentMonthLabel(): string {
  const all = listDates();
  if (!all.length) return '';
  const [y, m] = all[0].split('-').map(Number);
  return `${y} 年 ${m} 月`;
}
