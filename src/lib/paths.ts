const base = import.meta.env.BASE_URL.replace(/\/$/, '');

/** Prefix a site-absolute path ("/labs/") with the deploy base. */
export const withBase = (path: string) => `${base}${path}`;

export const labUrl = (id: string) => withBase(`/labs/${id}/`);
