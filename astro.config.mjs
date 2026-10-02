import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import { unified } from '@astrojs/markdown-remark';
import remarkDirective from 'remark-directive';
import remarkLabDirectives from './src/plugins/remark-lab-directives.mjs';
import remarkBaseLinks from './src/plugins/remark-base-links.mjs';
import rehypeFigures from './src/plugins/rehype-figures.mjs';

// Project pages live under /<repo>/; a custom domain sets BASE_PATH=/.
const base = process.env.BASE_PATH || '/BESSER-education';
const site = process.env.SITE_URL || 'https://besser-pearl.github.io';

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  integrations: [react()],
  markdown: {
    processor: unified({
      remarkPlugins: [remarkDirective, remarkLabDirectives, [remarkBaseLinks, { base }]],
      rehypePlugins: [rehypeFigures],
    }),
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark-dimmed' },
      defaultColor: false,
      wrap: false,
    },
  },
});
