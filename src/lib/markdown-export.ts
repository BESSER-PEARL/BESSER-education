import type { Lab } from './labs';
import { formatDuration } from './labs';
import { trackById } from '../data/tracks';

// Titles match remark-lab-directives.mjs so the export reads like the site.
const BLOCK_TITLES: Record<string, string> = {
  note: 'Note',
  tip: 'Tip',
  caution: 'Before you continue',
  checkpoint: 'Check your work',
  exercise: 'Exercise',
  troubleshoot: 'If something goes wrong',
};

const siteRoot = () => (import.meta.env.SITE ?? '').replace(/\/$/, '') + import.meta.env.BASE_URL.replace(/\/$/, '');

/** Rewrite one line of prose (not code): inline helpers, site links, image paths. */
function inline(line: string, labId: string, root: string): string {
  return line
    .replace(/:ui\[([^\]]+)\]/g, '**$1**')
    .replace(/:kbd\[([^\]]+)\]/g, '<kbd>$1</kbd>')
    .replace(/\]\(\.\/([^)\s]+)/g, `](${root}/labs/${labId}/$1`)
    .replace(/\]\(\/(?!\/)/g, `](${root}/`);
}

/** Convert a lab's site Markdown into plain GitHub-flavoured Markdown. */
function convertBody(body: string, labId: string, root: string): string {
  const out: string[] = [];
  let fence: string | null = null;
  let block: { kind: string; label: string } | null = null;
  let step = 0;

  // Inside a quote-style block every line gets a "> " prefix.
  const push = (line: string) => {
    if (block && block.kind !== 'solution') out.push(line ? `> ${line}` : '>');
    else out.push(line);
  };

  for (const raw of body.replace(/<!--[\s\S]*?-->\n?/g, '').split('\n')) {
    const fenceMatch = raw.match(/^\s*(`{3,}|~{3,})/);
    if (fenceMatch) {
      if (!fence) fence = fenceMatch[1];
      else if (raw.trim().startsWith(fence)) fence = null;
      push(raw);
      continue;
    }
    if (fence) {
      push(raw);
      continue;
    }

    const open = raw.match(/^:::(\w+)(?:\[(.*)\])?\s*$/);
    if (open && !block) {
      const [, kind, label = ''] = open;
      block = { kind, label };
      if (kind === 'solution') {
        out.push('<details>', `<summary>${label || 'Show a solution'}</summary>`, '');
      } else {
        const title = BLOCK_TITLES[kind] ?? kind;
        const heading = kind === 'exercise' && label ? `${title}: ${label}` : label || title;
        out.push(`> **${heading}**`, '>');
      }
      continue;
    }
    if (/^:::\s*$/.test(raw) && block) {
      if (block.kind === 'solution') out.push('', '</details>');
      block = null;
      continue;
    }

    const h2 = raw.match(/^## (.+)$/);
    if (h2 && !block) {
      step += 1;
      out.push(`## ${step}. ${inline(h2[1], labId, root)}`);
      continue;
    }
    push(inline(raw, labId, root));
  }
  return out.join('\n').replace(/\n{3,}/g, '\n\n').trim();
}

export function labToMarkdown(lab: Lab, all: Lab[], headingLevel = 1): string {
  const root = siteRoot();
  const d = lab.data;
  const h = '#'.repeat(headingLevel);
  const before = d.before
    .map((id) => all.find((l) => l.id === id))
    .filter((l): l is Lab => Boolean(l))
    .map((l) => `[Lab ${l.data.number}](${root}/labs/${l.id}/)`)
    .join(', ');
  const updated = d.updated.toISOString().slice(0, 10);

  const head = [
    `${h} Lab ${d.number}: ${d.title}`,
    '',
    d.summary,
    '',
    '| Time | Level | Runs with | Do first | Track |',
    '| --- | --- | --- | --- | --- |',
    `| ${formatDuration(d.duration)} | ${d.level} | ${d.setup.join(', ')} | ${before || 'Nothing'} | ${trackById[d.track].name} |`,
    '',
    "**You'll learn to**",
    '',
    ...d.outcomes.map((o) => `- ${o}`),
    '',
    "**You'll need**",
    '',
    ...d.needs.map((n) => `- ${n}`),
    '',
    ...(d.files.length
      ? ['**Files for this lab**', '', ...d.files.map((f) => `- [${f.label}](${root}${f.href})`), '']
      : []),
    `Online version: ${root}/labs/${lab.id}/`,
    '',
    '---',
    '',
  ];

  // Shift the lab's own headings down when several labs share one file.
  let body = convertBody(lab.body ?? '', lab.id, root);
  if (headingLevel > 1) {
    const extra = '#'.repeat(headingLevel - 1);
    body = body.replace(/^(#{2,6}) /gm, `${extra}$1 `);
  }

  return [...head, body, '', '---', '', `Checked against BESSER ${d.version} on ${updated}.`, ''].join('\n');
}

export function allLabsToMarkdown(labs: Lab[]): string {
  const root = siteRoot();
  const toc = labs.map((l) => `${l.data.number}. [${l.data.title}](#lab-${l.data.number}) (${formatDuration(l.data.duration)})`);
  const parts = labs.map((l) => `<a id="lab-${l.data.number}"></a>\n\n${labToMarkdown(l, labs, 2)}`);
  return [
    '# BESSER Labs',
    '',
    `Hands-on labs for the BESSER low-code platform. Online version: ${root}/`,
    '',
    ...toc,
    '',
    '---',
    '',
    parts.join('\n\n'),
  ].join('\n');
}
