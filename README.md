# BESSER Education

**Hands-on guides and exercises for the BESSER ecosystem.**

Welcome! This repository is a self-paced course for learning the [BESSER low-code platform (BLC)](https://github.com/BESSER-PEARL/BESSER) and the [BESSER Agentic Framework (BAF)](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework). It's organized as a sequence of **six labs** that take you from your first B-UML model to a full-stack web application deployed to the cloud, with a conversational agent inside.

Whether you are a beginner to low-code or an advanced developer, each lab is a standalone unit you can tackle on its own — but doing them in order gives you the smoothest path.

---

## Prerequisites

- **Python 3.11+** for every lab that runs code
- **A modern browser** for the labs using the Web Modeling Editor
- **Docker Desktop** (for Lab 2's local deployment)
- **Free GitHub & Render accounts** (for Lab 6's cloud deployment)
- Core libraries:
  ```bash
  pip install besser[all]
  pip install besser-agentic-framework[all]
  ```

No prior BESSER experience is assumed. Basic UML / Python literacy is enough to get started.

---

## Lab overview

| # | Lab | Track |
|---|---|---|
| 1 | [BESSER Basics](lab1_besser_basics/README.md) | BLC |
| 2 | [Full Application with the WME](lab2_web_modeling_editor/README.md) | BLC |
| 3 | [Developing a Code Generator](lab3_developing_code_generators/README.md) | BLC |
| 4 | [Metamodeling and Advanced Generators](lab4_metamodeling_and_code_generators/README.md) | BLC |
| 5 | [Building Agents with BAF](lab5_besser_agentic_framework/README.md) | BAF |
| 6 | [From Modeling to Deployment](lab6_render_deployment/README.md) | BLC + BAF |

---

## What each lab covers

### Lab 1 — BESSER Basics *(BLC)*

Your first contact with B-UML. Create a class diagram in Python, then again in the Web Modeling Editor, then use built-in code generators to produce SQLAlchemy models and a Django project.

**You'll produce:** a Python domain model, a SQLite database, a runnable Django app.

### Lab 2 — Building a Full Application with the BESSER WME *(BLC)*

End-to-end low-code workflow inside the Web Modeling Editor. Model a digital-twin domain, design a chatbot as a state machine, build a no-code UI, generate a full web application, and deploy it locally with Docker Compose.

**You'll produce:** a running full-stack app (FastAPI + React + SQLite), populated via the generated REST API.

### Lab 3 — Developing a Code Generator *(BLC)*

Switch perspective from user to developer. Subclass `GeneratorInterface`, write a Jinja2 template, and build a custom **Ruby on Rails** generator that turns any B-UML structural model into idiomatic Rails `ApplicationRecord` classes with associations.

**You'll produce:** a custom `RailsGenerator` that emits `models.rb` from any B-UML model.

### Lab 4 — Metamodeling and Advanced Generators *(BLC)*

Go deeper: extend the B-UML metamodel itself, then propagate the change through BESSER's built-in generators. Two exercises: add an `is_unique` property flag and update the SQLAlchemy generator, and add class-method support to the Java generator.

**You'll produce:** a patched BESSER install with new metamodel features and matching generator output.

### Lab 5 — Building Agents with BAF *(BAF)*

Build intelligent agents with the BESSER Agentic Framework. Cover state machines, LLM-backed intent classification, Retrieval-Augmented Generation (RAG) over PDFs, a no-code agent generator from CSV, and custom message processors.

**You'll produce:** a RAG-powered chatbot and a Streamlit app that generates new agents from data.

### Lab 6 — From Modeling to Deployment *(BLC + BAF)*

Capstone lab: put it all together. Use class diagrams, agent diagrams, and the GUI editor to design a library-management system, generate a full app, push to GitHub, and deploy to Render. The final artifact is a live, shareable web app with an integrated agent.

**You'll produce:** a publicly deployed full-stack web application on Render.

---

## Suggested paths

| Your goal | Recommended order |
|---|---|
| **Learn BESSER from scratch** | 1 → 2 → 3 → 4 → 5 → 6 |
| **Just low-code app building** | 1 → 2 → 6 |
| **Just agent building** | 5 (optionally 2 for the WME's agent editor) |
| **Generator / metamodel development** | 1 → 3 → 4 |
| **Deploy something quickly** | 1 → 2 → 6 |

---

## Solutions for educators

A private repository with full solutions to every exercise is available to instructors. To request access, email us at **info@besser-pearl.org**.

---

## Getting help

- **Documentation**
  - [BESSER low-code platform](https://besser.readthedocs.io/en/latest/)
  - [BESSER Agentic Framework](https://besser-agentic-framework.readthedocs.io/latest/)
- **Source code**
  - [BESSER on GitHub](https://github.com/BESSER-PEARL/BESSER)
  - [BAF on GitHub](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework)
- **Web Modeling Editor:** https://editor.besser-pearl.org/
- **Contact:** info@besser-pearl.org

---

## License

See [LICENSE](LICENSE).
