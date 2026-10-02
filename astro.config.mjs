import { defineConfig } from 'astro/config';
import { cp, readdir } from 'node:fs/promises';
import react from '@astrojs/react';
import { unified } from '@astrojs/markdown-remark';
import remarkDirective from 'remark-directive';
import remarkLabDirectives from './src/plugins/remark-lab-directives.mjs';
import remarkBaseLinks from './src/plugins/remark-base-links.mjs';
import rehypeFigures from './src/plugins/rehype-figures.mjs';

// Served from the custom domain labs.besser-pearl.org. To serve from
// besser-pearl.github.io/BESSER-education instead, set BASE_PATH=/BESSER-education.
const base = process.env.BASE_PATH || '/';
const site = process.env.SITE_URL || 'https://labs.besser-pearl.org';

// The Markdown exports link to the original screenshots, so publish them at /labs/<id>/<file>.
const labImages = {
  name: 'lab-images',
  hooks: {
    'astro:build:done': async ({ dir }) => {
      const src = new URL('./src/content/labs/', import.meta.url);
      for (const lab of await readdir(src, { withFileTypes: true })) {
        if (!lab.isDirectory() || lab.name.startsWith('_')) continue;
        for (const file of await readdir(new URL(`${lab.name}/`, src))) {
          if (/\.(png|jpe?g|gif|webp|svg)$/i.test(file)) {
            await cp(new URL(`${lab.name}/${file}`, src), new URL(`labs/${lab.name}/${file}`, dir));
          }
        }
      }
    },
  },
};

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  integrations: [react(), labImages],
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
