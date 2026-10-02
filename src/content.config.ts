import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const labs = defineCollection({
  // Each lab is a folder: src/content/labs/<slug>/index.md, with its images beside it.
  // Folders starting with "_" (like the template) are ignored.
  loader: glob({
    pattern: '[!_]*/index.md',
    base: './src/content/labs',
    generateId: ({ entry }) => entry.split('/')[0],
  }),
  schema: z.object({
    title: z.string(),
    number: z.number().int().positive(),
    track: z.enum(['foundations', 'ai', 'data', 'apps', 'agents', 'extend']),
    /** One sentence: what the learner ends up with. */
    summary: z.string(),
    /** Minutes, for a first-time learner. */
    duration: z.number().int().positive(),
    level: z.enum(['Beginner', 'Intermediate', 'Advanced']),
    /** Where the lab runs: drives the filters on the labs index. */
    setup: z.array(z.enum(['Browser', 'Python', 'Docker', 'GitHub', 'API key'])).min(1),
    /** Shown under "You'll need". */
    needs: z.array(z.string()).min(1),
    /** Shown under "You'll learn to". */
    outcomes: z.array(z.string()).min(1),
    /** Lab ids (folder names) to do first. */
    before: z.array(z.string()).default([]),
    /** Files the learner downloads, relative to /public. */
    files: z.array(z.object({ label: z.string(), href: z.string() })).default([]),
    updated: z.coerce.date(),
    /** BESSER release the steps were checked against. */
    version: z.string(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { labs };
