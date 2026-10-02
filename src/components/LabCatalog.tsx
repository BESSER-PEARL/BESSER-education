import { useEffect, useState } from 'react';

export interface CatalogLab {
  id: string;
  href: string;
  number: number;
  title: string;
  summary: string;
  duration: string;
  level: string;
  setup: string[];
  track: string;
}

export interface CatalogTrack {
  id: string;
  name: string;
  description: string;
}

interface Props {
  labs: CatalogLab[];
  tracks: CatalogTrack[];
}

const FILTERS = [
  { id: 'all', label: 'All labs', test: () => true },
  { id: 'browser', label: 'Browser only', test: (l: CatalogLab) => l.setup.every((s) => s === 'Browser' || s === 'GitHub') },
  { id: 'python', label: 'Uses Python', test: (l: CatalogLab) => l.setup.includes('Python') },
  { id: 'docker', label: 'Uses Docker', test: (l: CatalogLab) => l.setup.includes('Docker') },
  { id: 'key', label: 'Needs an API key', test: (l: CatalogLab) => l.setup.includes('API key') },
] as const;

type FilterId = (typeof FILTERS)[number]['id'];

export default function LabCatalog({ labs, tracks }: Props) {
  const [filter, setFilter] = useState<FilterId>('all');
  const [done, setDone] = useState<Set<string>>(new Set());

  useEffect(() => {
    const ids = new Set<string>();
    for (const l of labs) {
      try {
        if (JSON.parse(localStorage.getItem(`besser-labs:progress:${l.id}`) ?? 'null')?.complete) ids.add(l.id);
      } catch {}
    }
    setDone(ids);
  }, [labs]);

  const test = FILTERS.find((f) => f.id === filter)!.test;
  const shown = labs.filter(test);

  return (
    <div className="catalog">
      <div className="catalog__filters" role="group" aria-label="Filter labs">
        {FILTERS.map((f) => (
          <button
            key={f.id}
            type="button"
            className="chip"
            aria-pressed={filter === f.id}
            onClick={() => setFilter(f.id)}
          >
            {f.label}
            <span className="chip__count">{labs.filter(f.test).length}</span>
          </button>
        ))}
      </div>
      <p className="catalog__status" aria-live="polite">
        {filter === 'all' ? `${labs.length} labs` : `${shown.length} of ${labs.length} labs`}
      </p>

      {tracks.map((t) => {
        const rows = shown.filter((l) => l.track === t.id);
        if (!rows.length) return null;
        return (
          <section key={t.id} id={t.id} className="catalog__track">
            <header className="catalog__track-head">
              <h2>{t.name}</h2>
              <p>{t.description}</p>
            </header>
            <ol className="catalog__rows">
              {rows.map((l) => (
                <li key={l.id} className="row">
                  <span className="row__num" data-done={done.has(l.id) || undefined}>
                    {String(l.number).padStart(2, '0')}
                  </span>
                  <div className="row__main">
                    <h3 className="row__title">
                      <a href={l.href}>{l.title}</a>
                    </h3>
                    <p className="row__summary">{l.summary}</p>
                  </div>
                  <dl className="row__meta">
                    <div>
                      <dt>Time</dt>
                      <dd>{l.duration}</dd>
                    </div>
                    <div>
                      <dt>Level</dt>
                      <dd>{l.level}</dd>
                    </div>
                    <div>
                      <dt>Runs with</dt>
                      <dd>{l.setup.join(', ')}</dd>
                    </div>
                  </dl>
                </li>
              ))}
            </ol>
          </section>
        );
      })}
    </div>
  );
}
