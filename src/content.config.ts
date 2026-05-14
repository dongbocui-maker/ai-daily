import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const sevenPillars = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/seven-pillars' }),
  schema: z.object({
    order: z.number(),
    slug: z.string(),
    docNum: z.string(),
    docColor: z.enum(['foundation', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'conclusion']),
    title: z.string(),
    feishuToken: z.string(),
    words: z.string().optional(),
  }),
});

export const collections = { 'seven-pillars': sevenPillars };
