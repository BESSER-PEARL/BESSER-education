import { useEffect, useMemo, useState } from 'react';

interface Step {
  slug: string;
  text: string;
}

interface Props {
  labId: string;
  steps: Step[];
}

interface Saved {
  done: string[];
  complete: boolean;
}

const key = (id: string) => `besser-labs:progress:${id}`;

function load(id: string): Saved {
  try {
    const raw = JSON.parse(localStorage.getItem(key(id)) ?? 'null');
    if (raw && Array.isArray(raw.done)) return { done: raw.done, complete: !!raw.complete };
  } catch {}
  return { done: [], complete: false };
}

function save(id: string, value: Saved) {
  try {
    localStorage.setItem(key(id), JSON.stringify(value));
  } catch {}
}

/** Step list with per-step ticks, kept in this browser only. */
export default function LabProgress({ labId, steps }: Props) {
  const [done, setDone] = useState<Set<string>>(new Set());
  const [ready, setReady] = useState(false);
  const [open, setOpen] = useState(false);
  const [current, setCurrent] = useState<string | null>(null);

  useEffect(() => {
    setDone(new Set(load(labId).done));
    setReady(true);
  }, [labId]);

  useEffect(() => {
    if (!ready) return;
    const complete = steps.length > 0 && steps.every((s) => done.has(s.slug));
    save(labId, { done: [...done], complete });
  }, [done, ready, labId, steps]);

  // Highlight the step being read.
  useEffect(() => {
    const els = steps.map((s) => document.getElementById(s.slug)).filter(Boolean) as HTMLElement[];
    if (!els.length || !('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]) setCurrent(visible[0].target.id);
      },
      { rootMargin: '-80px 0px -65% 0px' },
    );
    els.forEach((el) => io.observe(el));
    return () => io.disconnect();
  }, [steps]);

  const count = useMemo(() => steps.filter((s) => done.has(s.slug)).length, [steps, done]);
  const allDone = steps.length > 0 && count === steps.length;

  const toggle = (slug: string) =>
    setDone((prev) => {
      const next = new Set(prev);
      next.has(slug) ? next.delete(slug) : next.add(slug);
      return next;
    });

  return (
    <nav className="progress" aria-label="Steps in this lab" data-open={open}>
      <button type="button" className="progress__toggle" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        <span>Steps</span>
        <span className="progress__count">
          {count} of {steps.length} done
        </span>
      </button>
      <p className="progress__heading">
        Steps <span className="progress__count">{count} of {steps.length} done</span>
      </p>
      <div className="progress__bar" aria-hidden="true">
        <span style={{ width: `${steps.length ? (count / steps.length) * 100 : 0}%` }} />
      </div>
      <ol className="progress__list">
        {steps.map((s, i) => {
          const isDone = done.has(s.slug);
          return (
            <li key={s.slug} data-current={current === s.slug || undefined} data-done={isDone || undefined}>
              <input
                type="checkbox"
                id={`done-${s.slug}`}
                checked={isDone}
                onChange={() => toggle(s.slug)}
                aria-label={`Mark step ${i + 1} as done`}
              />
              <a href={`#${s.slug}`} onClick={() => setOpen(false)}>
                <span className="progress__n">{i + 1}</span>
                {s.text}
              </a>
            </li>
          );
        })}
      </ol>
      {allDone && <p className="progress__complete">Lab complete. It's ticked off on the home page too.</p>}
      {count > 0 && (
        <button type="button" className="progress__reset" onClick={() => setDone(new Set())}>
          Clear my progress
        </button>
      )}
    </nav>
  );
}
