# Lab 6 — From Modeling to Deployment with BESSER

## At a glance

- **You'll learn:** How to go from a BESSER model to a **publicly deployed** full-stack web application using the BESSER Web Modeling Editor, GitHub integration, and Render cloud hosting.
- **You'll produce:** A live library-management web app with a class diagram, an integrated chatbot, an auto-generated React UI, and a Render deployment URL you can share.
- **You'll need first:** [Lab 2 — Building a Full Application with the WME](../lab2_web_modeling_editor/README.md) for the modeling basics; [Lab 5 — BAF](../lab5_besser_agentic_framework/README.md) helps with the agent portion.

---

## Prerequisites

- Access to the [BESSER Web Modeling Editor](https://editor.besser-pearl.org/) (no installation required)
- A free [GitHub account](https://github.com/) (code hosting + deployment integration)
- A free [Render account](https://render.com/) (cloud deployment)
- Basic familiarity with web applications, REST APIs, and UML class diagrams

---

## 1. Context

Modern web application development typically requires expertise in multiple technologies — frontend frameworks, backend APIs, databases, and deployment infrastructure. Low-code platforms like BESSER dramatically simplify this by letting you **model** your application's structure and **automatically generate** all the plumbing.

BESSER's **Full Web App Generator** produces a complete application stack from your models:

- **Backend** — FastAPI with SQLAlchemy ORM and Pydantic validation
- **Frontend** — React with TypeScript, forms, tables, and charts
- **Database** — SQLite by default, configurable to PostgreSQL or MySQL
- **Deployment** — Docker containers orchestrated with Docker Compose
- **Smart features** — optional conversational agent integration

<div align="center">
  <img src="figs/besser_overview.png" alt="BESSER Overview" width="700"/>
</div>

The end-to-end workflow in this lab:

1. **Model** — Design your application as multiple models (class diagram, agent, GUI)
2. **Generate** — BESSER produces the full app code
3. **Push to GitHub** — BESSER creates a repo under your account and pushes the generated code
4. **Deploy on Render** — BESSER hands off to Render for free-tier cloud hosting

---

## 2. Scenario

You will build a **Library Management System** with an integrated chatbot that answers common questions. The domain:

| Class | Attributes |
|---|---|
| `Library` | `name`, `address`, `webPage`, `telephone` |
| `Book` | `title`, `pages`, `stock`, `price`, `releaseDate`, `genre` |
| `Author` | `name`, `birthDate`, `email` |

A `Library` has many `Book`s; a `Book` can have multiple `Author`s (many-to-many). An OCL constraint ensures every book has more than 10 pages.

You will combine three perspectives:

- A **class diagram** defining the domain / database
- An **agent diagram** defining the library assistant chatbot
- A **GUI model** auto-generated from the class diagram and augmented with the agent

---

## 3. Walkthrough

### 3.1 Create a blank project

1. Navigate to [editor.besser-pearl.org](https://editor.besser-pearl.org/).
2. Click **Create Blank Project** (or **File → New Project**).
3. Give your project a name (e.g. `Library Management System`), owner, and description.
4. Click **Create Project**.

<div align="center">
  <img src="figs/besser_new_project.png" alt="Create Blank Project" width="400"/>
</div>

### 3.2 Load the Library class diagram template

A project in BESSER is composed of several models that describe different parts of the application. **Class diagrams** define the structure of the database.

1. Click **File → Load Template**.
2. Select **Class Diagram**, choose **Library**, and click **Load Template**.

<div align="center">
  <img src="figs/library_class_diagram.png" alt="Library Class Diagram" width="700"/>
</div>

This diagram includes three main classes (`Library`, `Book`, `Author`) and a `Genre` enumeration. A `Library` stores basic information (name, web page, address, telephone) and manages a collection of books. A `Book` has attributes such as title, pages, stock, price, release date, and genre, and provides an operation to decrease its stock. An `Author` stores name and birth date. The relationships are one-to-many (library → books) and many-to-many (books ↔ authors). An OCL constraint requires every book to have more than 10 pages.

### 3.3 Load the Library agent template

BESSER provides a dedicated perspective for agents, based on a state machine extension. Let's load the library agent example.

1. Click **File → Load Template**.
2. Select **Agent Diagram**, choose **Library Agent**, and click **Load Template**.

<div align="center">
  <img src="figs/library_agent.png" alt="Library Agent Template" width="700"/>
</div>

This agent is a simple **library support bot**: it greets the user, then moves to an **Idle** state where it asks how it can assist. Several intents represent possible user requests (opening hours, cheapest book by an author, contact info to speak with a human). Each intent carries example user phrases used for matching. When an intent fires, the agent transitions to the corresponding state, replies, and returns to Idle.

### 3.4 Design the GUI

BESSER includes a visual GUI editor so you don't need to write frontend code manually.

Click the **GUI** perspective in the left-side menu. The no-code editor lets you drag and drop blocks, connect them with classes from the class diagram, and customize styles.

**Auto-generate the default GUI:**

1. In the GUI diagram editor, find the **Auto-Generate GUI from Class Diagram** button.
2. Click it — BESSER will create:
   - A page per class in your domain model
   - Table components for CRUD operations
   - Forms for create/edit
   - Navigation between pages

<div align="center">
  <img src="figs/gui.png" alt="Auto-Generate GUI" width="700"/>
</div>

The GUI model supports:

- **Tables** with CRUD operations
- **Charts** for data visualization
- **Navigation** between pages
- **Method buttons** for calling class methods
- **Chatbots** that hook into BAF agents
- Other widget blocks

**Add the agent to the GUI:**

1. Drag the **BESSER Agent** block from the palette on the right.
2. Drop it on a page, click it, and select the **Library Agent** you loaded in section 3.3.

The [BESSER Agentic Framework](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework) powers the conversational agent at runtime.

### 3.5 Validate your models

Before generating, make sure the models are valid.

1. Open the **class diagram** and click **Quality Check**. Fix any errors or warnings.
2. Repeat for the **Agent model**.

> **Note:** Quality Check is not yet available for the GUI model. That check is on the roadmap.

### 3.6 Connect GitHub

BESSER generates the full code for your app and pushes it to a new repository under your GitHub account. Click the **GitHub icon** in the upper-right corner of the editor and authorize.

<div align="center">
  <img src="figs/git_connection.png" alt="GitHub Connection" width="250"/>
</div>

### 3.7 Generate and deploy

1. Click **Deploy → Publish Web App to Render**.
2. Enter the name of the GitHub repository that will be created, add a description, and choose whether it should be private.
3. Click **Publish to Render**.

<div align="center">
  <img src="figs/git_conf.png" alt="GitHub Configuration" width="300"/>
</div>

BESSER generates the code, pushes it to your new repo, and hands off to Render. Click **View GitHub Repository** to inspect what was generated.

The repository structure:

```
agents/
  └── library_agent/
      └── ...
backend/
  ├── pydantic_classes.py
  ├── main_api.py
  └── ...
buml/
  └── ...
frontend/
  ├── src/
  ├── public/
  ├── vite.config.ts
  └── ...
docker-compose.yml
render.yaml
README.md
```

Back in the editor, click **Open Render Deployment**. Log in to Render, pick a **Blueprint** name, and click **Deploy Blueprint**.

<div align="center">
  <img src="figs/render_blueprint.png" alt="Render Blueprint" width="700"/>
</div>

Render's free tier uses small instances, so the initial deployment takes **4–12 minutes**. Three services are created: backend, frontend, and agent. Once they are all up, open **Resources**, pick the frontend service, and open the generated URL.

<div align="center">
  <img src="figs/app.png" alt="Web Application" width="700"/>
</div>

Test the app, the chatbot, and every CRUD screen.

---

## 4. Exercises

> **Exercise 4.1 — Extend the domain**
>
> Add a `Member` class to the Library model (attributes: `name`, `memberId`, `joinDate`). Create a many-to-many relationship between `Book` and `Member` to represent borrowing. Regenerate, push to GitHub, and redeploy to Render.

> **Exercise 4.2 — Teach the agent a new intent**
>
> Add an intent to the library agent: `check_book_availability`, triggered by phrases like "is X available?" or "do you have X?". Have it reply with a placeholder message. Redeploy and test.

---

## 5. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| **Deploy to Render** button does nothing | GitHub not connected | Click the GitHub icon and authorize the BESSER app |
| Render deployment hangs >15 minutes | Free tier is queued | Wait it out, or upgrade to a paid Render tier for dedicated runners |
| Frontend shows 502 / Bad Gateway on first load | Backend still starting up | Reload after ~1 minute; check backend service logs in the Render dashboard |
| Agent message block in GUI has no agent to choose | Agent diagram not saved | Save the agent model, reload the GUI editor, and reselect the agent |
| Generated repo pushed but no `render.yaml` | Older BESSER generator | Upgrade BESSER to the latest version and regenerate |
| Quality Check passes on class diagram but generation fails on OCL | Unsupported OCL construct | Simplify the constraint or remove it temporarily |

---

## 6. Support us

If this lab was useful and you'd like to support our work:

1. **Star our GitHub repository** — it helps others discover the project:
   https://github.com/BESSER-PEARL/BESSER

   <div align="center">
     <img src="figs/github_star.png" alt="GitHub Star" width="700"/>
   </div>

2. **Fill out a short survey (~5 minutes)** — your feedback shapes future materials:
   [Take the survey](https://docs.google.com/forms/d/e/1FAIpQLSdhYVFFu8xiFkoV4u6Pgjf5F7-IS_W7aTj34N5YS2L143vxoQ/viewform)

Thank you!

---

## 7. Summary

In this lab, you have learned how to:

- Use the BESSER Web Modeling Editor to load and modify class diagram, agent, and GUI templates
- Design a complete web application using three orthogonal model perspectives
- Integrate a conversational agent powered by BAF
- Generate production-ready code with BESSER's Full Web App Generator
- Deploy a full-stack web application to Render via GitHub integration

You now have the skills to go from a blank editor to a live, shareable web application in under 90 minutes. Congratulations on completing the BESSER Education track!

---

## Resources

- [BESSER documentation](https://besser.readthedocs.io/en/latest/)
- [BESSER Web Modeling Editor docs](https://besser.readthedocs.io/projects/besser-web-modeling-editor/en/latest/)
- [Full Web App generator docs](https://besser.readthedocs.io/en/latest/generators/full_web_app.html)
- [BESSER Agentic Framework docs](https://besser-agentic-framework.readthedocs.io/latest/)
- [Render documentation](https://render.com/docs)
- [Docker documentation](https://docs.docker.com/)
- [React documentation](https://react.dev/)
- [FastAPI documentation](https://fastapi.tiangolo.com/)
