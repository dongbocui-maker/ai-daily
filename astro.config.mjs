// @ts-check
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  site: 'https://jason-dongbo-cui-accent.github.io',
  base: '/ai-daily',
  trailingSlash: 'always',
  integrations: [tailwind(), sitemap()],
  build: {
    format: 'directory',
  },
});
