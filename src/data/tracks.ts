export type TrackId = 'foundations' | 'ai' | 'data' | 'apps' | 'agents' | 'extend';

export interface Track {
  id: TrackId;
  name: string;
  /** One sentence shown on the home page and the labs index. */
  description: string;
}

// Order here is the order on the home page.
export const tracks: Track[] = [
  {
    id: 'foundations',
    name: 'Modeling foundations',
    description: 'Draw a class diagram in the editor, then build the same model in Python.',
  },
  {
    id: 'ai',
    name: 'Build with AI',
    description: 'Describe what you want and let the assistant and the Spec-Driven Agent do the modeling and coding.',
  },
  {
    id: 'data',
    name: 'Data and databases',
    description: 'Turn a model into SQL schemas and ORM code, then run a REST backend on top.',
  },
  {
    id: 'apps',
    name: 'Full applications',
    description: 'Combine class, GUI and agent models into a web app, then put it online.',
  },
  {
    id: 'agents',
    name: 'Conversational agents',
    description: 'Design chatbots as state machines, add LLMs and RAG, and adapt them to their users.',
  },
  {
    id: 'extend',
    name: 'Extend BESSER',
    description: 'Write your own code generator and add new concepts to the metamodel.',
  },
];

export const trackById = Object.fromEntries(tracks.map((t) => [t.id, t])) as Record<TrackId, Track>;
