import { getCollection, type CollectionEntry } from 'astro:content';

export type Lab = CollectionEntry<'labs'>;

/** Published labs in curriculum order. Drafts show up in `astro dev` only. */
export async function getLabs(): Promise<Lab[]> {
  const labs = await getCollection('labs', ({ data }) => import.meta.env.DEV || !data.draft);
  return labs.sort((a, b) => a.data.number - b.data.number);
}

export const labNumber = (n: number) => String(n).padStart(2, '0');

export const formatDuration = (minutes: number) =>
  minutes < 60 ? `${minutes} min` : `${Math.floor(minutes / 60)} h${minutes % 60 ? ` ${minutes % 60} min` : ''}`;
