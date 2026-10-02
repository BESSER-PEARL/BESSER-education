import type { APIRoute } from 'astro';
import { getLabs, type Lab } from '../../lib/labs';
import { labToMarkdown } from '../../lib/markdown-export';

export async function getStaticPaths() {
  const labs = await getLabs();
  return labs.map((lab) => ({ params: { id: lab.id }, props: { lab, all: labs } }));
}

export const GET: APIRoute = ({ props }) => {
  const { lab, all } = props as { lab: Lab; all: Lab[] };
  return new Response(labToMarkdown(lab, all), {
    headers: { 'Content-Type': 'text/markdown; charset=utf-8' },
  });
};
