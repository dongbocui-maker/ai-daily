// GitHub 榜单数据加载

export interface GitHubRepo {
  rank: number;
  name: string;
  url: string;
  description: string;
  description_zh?: string;
  language?: string;
  stars: number;
  stars_period?: number;
  forks?: number;
  topics?: string[];
  pushed_at?: string;
  created_at?: string;
}

export interface BoardData {
  general: GitHubRepo[];
  ai: GitHubRepo[];
}

export interface YearlyBoardData {
  newborn: BoardData;
  fastest_growing: BoardData;
}

// === Vite glob：构建期内嵌 JSON ===

const dailyMods = import.meta.glob<BoardData>('../data/github/daily/*.json', { eager: true, import: 'default' });
const weeklyMods = import.meta.glob<BoardData>('../data/github/weekly/*.json', { eager: true, import: 'default' });
const monthlyMods = import.meta.glob<BoardData>('../data/github/monthly/*.json', { eager: true, import: 'default' });
const yearlyMods = import.meta.glob<YearlyBoardData>('../data/github/yearly/*.json', { eager: true, import: 'default' });

function pickLatest<T>(mods: Record<string, T>): { key: string; data: T } | null {
  const entries = Object.entries(mods)
    .map(([path, data]) => {
      const m = path.match(/([^/]+)\.json$/);
      return m ? { key: m[1], data } : null;
    })
    .filter((x): x is { key: string; data: T } => x !== null)
    .sort((a, b) => b.key.localeCompare(a.key));
  return entries[0] ?? null;
}

export function loadDaily() {
  return pickLatest(dailyMods);
}

export function loadWeekly() {
  return pickLatest(weeklyMods);
}

export function loadMonthly() {
  return pickLatest(monthlyMods);
}

export function loadYearly() {
  return pickLatest(yearlyMods);
}

// === Helpers ===

export function formatDateShort(date: string): string {
  return date; // YYYY-MM-DD 已经够短
}

export function formatWeekLabel(week: string): string {
  // YYYY-WXX → "2026 年第 18 周"
  const m = week.match(/^(\d{4})-W(\d{2})$/);
  if (!m) return week;
  return `${m[1]} 年第 ${parseInt(m[2], 10)} 周`;
}

export function formatMonthLabel(ym: string): string {
  const m = ym.match(/^(\d{4})-(\d{2})$/);
  if (!m) return ym;
  return `${m[1]} 年 ${parseInt(m[2], 10)} 月`;
}

export function formatYearLabel(y: string): string {
  return `${y} 年`;
}

// 格式化 stars 数字（10500 → "10.5k"，1234567 → "1.2M"）
export function formatStars(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}k`;
  return String(n);
}

// 相对时间（"3 天前"）
export function relativeTime(iso: string): string {
  const d = new Date(iso);
  const diff = Date.now() - d.getTime();
  const days = Math.floor(diff / (1000 * 60 * 60 * 24));
  if (days < 1) return '今天';
  if (days < 7) return `${days} 天前`;
  if (days < 30) return `${Math.floor(days / 7)} 周前`;
  if (days < 365) return `${Math.floor(days / 30)} 个月前`;
  return `${Math.floor(days / 365)} 年前`;
}

// 语言颜色（GitHub 风格）
export const languageColors: Record<string, string> = {
  TypeScript: '#3178c6',
  JavaScript: '#f1e05a',
  Python: '#3572A5',
  Rust: '#dea584',
  Go: '#00ADD8',
  Java: '#b07219',
  'C++': '#f34b7d',
  C: '#555555',
  'C#': '#178600',
  Ruby: '#701516',
  PHP: '#4F5D95',
  Shell: '#89e051',
  HTML: '#e34c26',
  CSS: '#563d7c',
  Vue: '#41b883',
  Swift: '#FA7343',
  Kotlin: '#A97BFF',
  Dart: '#00B4AB',
  Lua: '#000080',
  Solidity: '#AA6746',
};
