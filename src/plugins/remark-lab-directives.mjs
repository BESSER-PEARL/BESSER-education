import { visit, SKIP } from 'unist-util-visit';
import { toString } from 'mdast-util-to-string';

// Container blocks authors can use in a lab:  :::checkpoint ... :::
const BLOCKS = {
  note: 'Note',
  tip: 'Tip',
  caution: 'Before you continue',
  checkpoint: 'Check your work',
  exercise: 'Exercise',
  solution: 'Show a solution',
  troubleshoot: 'If something goes wrong',
};

// Inline helpers:  :ui[File > New Project]  and  :kbd[Ctrl+S]
const INLINE = { ui: 'span', kbd: 'kbd' };

function takeLabel(node) {
  const first = node.children[0];
  if (first?.type === 'paragraph' && first.data?.directiveLabel) {
    node.children.shift();
    return toString(first);
  }
  return '';
}

const el = (hName, className, children, extra = {}) => ({
  type: 'labElement',
  data: { hName, hProperties: { className, ...extra } },
  children,
});

const text = (value) => ({ type: 'text', value });

export default function remarkLabDirectives() {
  return (tree, file) => {
    visit(tree, (node, index, parent) => {
      if (node.type === 'containerDirective') {
        const title = BLOCKS[node.name];
        if (!title) {
          file.fail(`Unknown block ":::${node.name}". Use one of: ${Object.keys(BLOCKS).join(', ')}`, node);
        }
        const label = takeLabel(node);

        if (node.name === 'solution') {
          node.data = { hName: 'details', hProperties: { className: ['solution'] } };
          node.children = [
            el('summary', ['solution__summary'], [text(label || title)]),
            el('div', ['solution__body'], node.children),
          ];
          return;
        }

        const heading = node.name === 'exercise' && label ? `${title}: ${label}` : label || title;
        node.data = {
          hName: 'aside',
          hProperties: { className: ['callout', `callout--${node.name}`], 'data-kind': node.name },
        };
        node.children = [
          el('p', ['callout__title'], [text(heading)]),
          el('div', ['callout__body'], node.children),
        ];
        return;
      }

      if (node.type === 'textDirective' || node.type === 'leafDirective') {
        const tag = INLINE[node.name];
        if (tag && node.type === 'textDirective') {
          node.data = { hName: tag, hProperties: { className: [`inline-${node.name}`] } };
          return;
        }
        // Not ours, e.g. "ratio 2:1" or "Note:Something": put the text back.
        const restored = [text(`:${node.name}`), ...(node.children ?? [])];
        parent.children.splice(index, 1, ...restored);
        return [SKIP, index + restored.length];
      }
    });
  };
}
