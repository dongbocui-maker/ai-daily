import typography from '@tailwindcss/typography';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        // Accenture-inspired brand palette
        accent: {
          purple: '#A100FF',         // 主品牌紫
          'purple-deep': '#7500C0',  // 深紫
          'purple-light': '#C982FF', // 浅紫
          black: '#000000',
          ink: '#0F0F0F',
          gray: {
            900: '#1A1A1A',
            800: '#2D2D2D',
            700: '#4A4A4A',
            500: '#7A7A7A',
            300: '#CFCFCF',
            100: '#F2F2F2',
            50: '#FAFAFA',
          },
        },
        // Section accent colors (subtle, for category icons)
        category: {
          news: '#A100FF',      // 紫 - 热点新闻
          enterprise: '#00C8FF', // 青 - 企业实践
          coding: '#00E676',    // 绿 - AI Coding
          report: '#FFB300',    // 金 - 报告论文
        },
      },
      fontFamily: {
        sans: [
          'Inter',
          '"Source Han Sans SC"',
          '"Noto Sans SC"',
          '"PingFang SC"',
          '"Microsoft YaHei"',
          'system-ui',
          'sans-serif',
        ],
        display: [
          'Inter',
          '"Source Han Sans SC"',
          '"Noto Sans SC"',
          'system-ui',
          'sans-serif',
        ],
      },
      fontSize: {
        // Accenture-style hierarchy
        'display': ['clamp(2.5rem, 5vw, 4.5rem)', { lineHeight: '1.05', letterSpacing: '-0.02em', fontWeight: '700' }],
        'h1': ['clamp(2rem, 3.5vw, 3rem)', { lineHeight: '1.1', letterSpacing: '-0.015em', fontWeight: '700' }],
        'h2': ['clamp(1.5rem, 2.5vw, 2.25rem)', { lineHeight: '1.15', letterSpacing: '-0.01em', fontWeight: '600' }],
        'h3': ['clamp(1.25rem, 1.8vw, 1.5rem)', { lineHeight: '1.25', fontWeight: '600' }],
      },
      maxWidth: {
        '8xl': '88rem',
      },
    },
  },
  plugins: [typography],
};
