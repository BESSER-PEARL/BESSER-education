---
# Copy this folder to src/content/labs/<your-lab-id>/ and edit. The folder name becomes the URL.
title: Short task-shaped title
number: 99                # position in the curriculum; renumber freely
track: foundations        # foundations | ai | data | apps | agents | extend
summary: One sentence saying what the learner has at the end.
duration: 45              # minutes for a first-timer, honestly measured
level: Beginner           # Beginner | Intermediate | Advanced
setup: [Browser]          # any of: Browser, Python, Docker, GitHub, API key
needs:
  - A modern browser
outcomes:
  - Something the learner can do afterwards, starting with a verb
before: []                # lab ids to do first, e.g. [first-model]
files: []                 # downloads in /public, e.g. [{ label: "Starter model (JSON)", href: "/files/my-lab/model.json" }]
updated: 2026-10-02
version: "8.0.1"          # BESSER release you checked the steps against
draft: true               # drafts only show in `npm run dev`
---

One or two paragraphs of context: the scenario and why it matters. No heading here.

## First task, named as an action

Every `##` heading is a numbered step and appears in the progress rail. Keep steps to
things a learner can finish and check in five to ten minutes.

1. Use the exact labels from the interface: open :ui[File > New Project].
2. Keyboard keys look like :kbd[Ctrl+S].

![What the screen looks like after this step](./screenshot.png "Caption shown under the image")

:::checkpoint
What the learner should see now. Be concrete: "The class has three attributes and Quality
Check reports no errors."
:::

## Second task

:::note
A UML-style note for context that is useful but not required.
:::

:::caution
Anything that costs money, needs an account, or can't be undone.
:::

:::troubleshoot
The most common way this step fails, and what to do about it.
:::

## Exercise

:::exercise[Short name of the exercise]
An open task that applies what the lab taught, without step-by-step instructions.
:::

:::solution
A short hint or a partial solution. Full solutions live in the private educators repository.
:::
