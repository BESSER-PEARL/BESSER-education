import { visit } from 'unist-util-visit';

// Lets authors write site links as "/labs/first-model/" regardless of the deploy base.
export default function remarkBaseLinks({ base = '/' } = {}) {
  const prefix = base.replace(/\/$/, '');
  return (tree) => {
    if (!prefix) return;
    visit(tree, ['link', 'definition'], (node) => {
      if (node.url.startsWith('/') && !node.url.startsWith('//') && !node.url.startsWith(prefix + '/')) {
        node.url = prefix + node.url;
      }
    });
  };
}
