import type { APIRoute } from 'astro';
import { getLabs } from '../../lib/labs';
import { allLabsToMarkdown } from '../../lib/markdown-export';

export const GET: APIRoute = async () =>
  new Response(allLabsToMarkdown(await getLabs()), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
