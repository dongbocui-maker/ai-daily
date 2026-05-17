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

const claudeCodeDocs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/claude-code-docs' }),
  schema: z.object({
    slug: z.string(),
    title: z.string(),
    subtitle: z.string().optional(),
    sourceUrl: z.string().url(),
    sourceLabel: z.string(),
    updated: z.string().optional(),
  }),
});

export const collections = { 'seven-pillars': sevenPillars, 'claude-code-docs': claudeCodeDocs };
