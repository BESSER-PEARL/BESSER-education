import { visit } from 'unist-util-visit';

// ![alt](shot.png "Caption") on its own line becomes <figure> with a <figcaption>.
export default function rehypeFigures() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (node.tagName !== 'p' || !parent) return;
      const kids = node.children.filter((c) => !(c.type === 'text' && !c.value.trim()));
      if (kids.length !== 1 || kids[0].type !== 'element' || kids[0].tagName !== 'img') return;
      const img = kids[0];
      const caption = img.properties?.title;
      if (!caption) return;
      delete img.properties.title;
      img.properties.loading = 'lazy';
      parent.children[index] = {
        type: 'element',
        tagName: 'figure',
        properties: {},
        children: [
          img,
          { type: 'element', tagName: 'figcaption', properties: {}, children: [{ type: 'text', value: caption }] },
        ],
      };
    });
  };
}
