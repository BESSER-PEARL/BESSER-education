# BESSER Labs

Hands-on labs for the [BESSER low-code platform](https://github.com/BESSER-PEARL/BESSER) and the
[BESSER Agentic Framework](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework).

**Read the labs at https://besser-pearl.github.io/BESSER-education/**

Each lab is a guided exercise you can finish in one sitting: modeling in the Web Modeling Editor and in
Python, building with the modeling assistant and the Spec-Driven Agent, databases, full web apps and
deployment, conversational agents, and extending BESSER with your own generators.

## Repository layout

| Path | What it holds |
| --- | --- |
| `src/content/labs/<lab-id>/index.md` | One lab, written in Markdown, with its screenshots beside it |
| `src/content/labs/_template/` | The template for a new lab |
| `public/files/<lab-id>/` | Files learners download (models, starter code, configuration) |
| `src/` (everything else) | The site itself: Astro pages, React components, styles |
| `.github/workflows/pages.yml` | Builds every pull request and publishes `main` to GitHub Pages |

## Run the site locally

Requires Node.js 22.12 or newer.

```bash
npm install
npm run dev      # live preview at http://localhost:4321/BESSER-education/
npm run build    # production build into dist/
```

## Add or update a lab

See [Write a lab](https://besser-pearl.github.io/BESSER-education/write-a-lab/) on the site, or start from
`src/content/labs/_template/index.md`. In short: copy the template folder, write the steps using the exact
labels from the editor, add real screenshots, set `draft: false`, and open a pull request.

## For educators

Worked solutions to the exercises live in a private repository. If you teach with these labs, contact
info@besser-pearl.org from your institutional address.

## Publishing

The workflow deploys with GitHub Pages' "GitHub Actions" source (Settings > Pages > Build and deployment >
Source: GitHub Actions). For a custom domain, set the repository variables `BASE_PATH` to `/` and
`SITE_URL` to the domain's URL.

## License

See [LICENSE](LICENSE).
