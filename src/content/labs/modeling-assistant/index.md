---
title: Model by conversation with the Modeling Assistant
number: 4
track: ai
summary: A clinic appointment model with a class diagram, an OCL constraint and a state machine, built and checked entirely through the Modeling Assistant chat.
duration: 35
level: Beginner
setup: [Browser]
needs:
  - A modern desktop browser (Chrome, Edge or Firefox)
  - Lab 1 (Your first class diagram) or equivalent familiarity with the editor canvas
outcomes:
  - Start a project in the Describe it (agentic) interface
  - Create a class diagram from a plain-language description
  - Refine a model with follow-up prompts and undo an assistant edit with Ctrl+Z
  - Verify what the assistant changed on the canvas and with Quality Check
  - Add a state machine and trigger a code generator from the chat
before: [first-model]
files: []
updated: 2026-10-02
version: "8.0"
draft: false
---

In Lab 1 you drew every class and association by hand. The Web Modeling Editor also has an agentic interface: you describe what you want in plain words, and the Modeling Assistant creates and edits the diagrams on the live canvas. The diagrams it produces are ordinary B-UML models, so everything you learned on the canvas still applies, and you can switch between chatting and drawing at any time.

In this lab you model a small clinic: patients book appointments with doctors. You build the class diagram by conversation, refine it, add a rule, add a state machine for the appointment lifecycle, and generate a PostgreSQL schema, all from the chat. Throughout, you check the result yourself instead of trusting the reply.

:::note
The assistant runs on a separate BESSER service. On [editor.besser-pearl.org](https://editor.besser-pearl.org) it is hosted for you and needs no API key or account; requests are rate limited per browser tab. Your messages and a snapshot of the current project are sent to that service so it can answer. The project itself stays in your browser's storage, as in Lab 1. Do not paste personal or confidential data into the chat.
:::

## Start a project in Describe it mode

1. Open [https://editor.besser-pearl.org](https://editor.besser-pearl.org). On a first visit the editor asks how you want to build.
2. On the :ui[Describe it] card, click :ui[Start describing].

![The first-run screen with two cards, Model it and Describe it, and a Free hosted Qwen pill on the Describe it card](./interface-choice.png "Describe it opens the agentic workspace; Model it opens the canvas you used in Lab 1")

3. The :ui[Create A Project] form opens with :ui[Agentic] already selected under :ui[View]. Enter the name `Clinic Appointments` and click :ui[Create Project]. The editor stores it as `Clinic_Appointments`.

![The Create A Project form with the name field, owner, description and the View toggle set to Agentic](./create-project-agentic.png "Agentic is preselected because you came from Describe it")

4. The assistant workspace fills the screen with the question "What would you like to create today?" and a composer that reads "Describe what you want to create or modify...". Next to the subtitle a dot shows the connection state.

![The assistant workspace with the headline, a Connected indicator, the composer and three example prompts](./describe-workspace.png "Green Connected means the hosted assistant is reachable. The example prompts under the composer change between visits")

:::note
If the editor opens straight into the canvas (because you ticked "Remember my choice" earlier, or already have projects), use :ui[File > New Project], choose :ui[Agentic] under :ui[View], and create the project there. Adding `?mode=agent` to the editor URL also opens the assistant workspace.
:::

:::checkpoint
The top bar shows the project name `Clinic_Appointments`, the workspace says :ui[Connected] with a green dot, and the line under the composer reads "Free to use with our hosted Qwen model."
:::

## Describe the clinic and let the assistant build the class diagram

1. Click into the composer, type the following prompt exactly, and press :kbd[Enter]:

```text
Create a class diagram for a clinic appointment system with the classes Patient, Doctor and Appointment. A patient can book many appointments, and each appointment is with exactly one doctor. Give each class a few attributes.
```

2. Wait for the reply. It usually arrives within half a minute. The assistant marks it with a badge such as :ui[System created] and offers quick-action chips under it, for example :ui[Generate application], :ui[Explain the specs] and :ui[Review the model].

<!-- TODO screenshot: assistant reply to the clinic prompt with the "System created" badge and the chips under it (assistant-create-reply.png). Not captured: on 2026-10-02 the hosted assistant on editor.besser-pearl.org returned only the degraded fallback reply (see troubleshoot below). -->

:::note
The wording of the reply, the attribute names and the layout differ from run to run, because a language model writes them. That is expected. What you check in this lab is the model, not the text: which classes, attributes and associations exist on the canvas.
:::

:::troubleshoot
**The reply says "I had a bit of trouble building everything at once, but I set up 3 item(s)..." and each class only has `+ id: str`.** The assistant fell back to placeholder classes because its language-model call failed on the server. The same happens if every follow-up returns "I couldn't process that modification. Please try again or rephrase your request." This is a service problem, not a problem with your prompt. Wait a few minutes and click :ui[New Chat] to try again, or continue the lab on the canvas: add the attributes and associations by hand as in [Lab 1](/labs/first-model/), then come back to the chat for the later steps.
:::

:::checkpoint
The chat shows your prompt, a reply naming Patient, Doctor and Appointment, and at least the :ui[Review the model] chip.
:::

## Switch to the canvas and verify what the assistant built

The assistant edits the model you see on the canvas. Look at the canvas after every change.

1. Click the :ui[Review the model] chip. It does not send a message; it closes the assistant workspace so you see the canvas. You can also click the :ui[See the Specs] tab at the bottom of the workspace, or press :kbd[Esc].
2. The Class editor shows the new diagram. Check:
   - There are three classes: `Patient`, `Doctor` and `Appointment`, each with several typed attributes.
   - There is an association between `Patient` and `Appointment` with a many end (`*` or `0..*`) on the Appointment side.
   - There is an association between `Appointment` and `Doctor` with multiplicity `1` on the Doctor side.
3. Double-click an association to open its properties and read the exact multiplicities, as you did in Lab 1.

<!-- TODO screenshot: the clinic class diagram on the canvas after Review the model, showing Patient, Doctor, Appointment and both associations (clinic-class-diagram.png). -->

4. To return to the chat, click the :ui[Describe your app] tab at the top of the canvas. The conversation is still there. In the low-code view the same assistant is also available from the round assistant button in the bottom-right corner (:ui[Open assistant]); both share one conversation.
5. In the workspace's bottom bar, click :ui[Your model]. It opens a recap of the data model and its relationships, derived from the project. Click it again to close it.

:::checkpoint
You can move between chat and canvas with :ui[Describe your app] and :ui[See the Specs], and the canvas shows the three classes connected by two associations with the multiplicities from your prompt. If a multiplicity is wrong, note it; you fix it in the next step.
:::

## Refine the model with follow-up prompts

Small, specific prompts work best. Name the class and the attribute, and say what must stay unchanged.

1. Send:

```text
Add an integer attribute named duration_minutes to the Appointment class.
```

2. Send:

```text
Rename the Doctor class to Physician.
```

3. Close the workspace and check both edits on the canvas: `Appointment` has `+ duration_minutes: int`, and the class formerly called `Doctor` is now `Physician`, still connected to `Appointment`.
4. Undo the rename. Click an empty spot on the canvas so it has focus, then press :kbd[Ctrl+Z] (:kbd[Cmd+Z] on macOS). Assistant edits go through the editor's normal undo stack. Check that the class is called `Doctor` again. If you pressed it once too often and `duration_minutes` disappeared as well, press :kbd[Ctrl+Y] or ask the assistant to add it again.
5. Open the chat again and add a rule. The assistant only writes OCL when you ask for a constraint explicitly:

```text
Add a constraint that the duration_minutes of an Appointment must be greater than 0.
```

6. On the canvas, an OCL constraint box is attached to `Appointment`. Double-click it and read the expression. It should be equivalent to `context Appointment inv: self.duration_minutes > 0`; the constraint name and exact formatting may differ.

<!-- TODO screenshot: the Appointment class with duration_minutes and the attached OCL constraint box (appointment-constraint.png). -->

:::checkpoint
`Appointment` has `duration_minutes: int`, the class is named `Doctor` again after the undo, and an OCL constraint on `Appointment` requires `duration_minutes` to be greater than 0.
:::

## Ask the assistant to explain the model

The assistant can describe the current model in words. This is a quick way to spot a misunderstanding, but it is a summary, not a check.

1. Send:

```text
Describe my current model.
```

2. Compare the description with the canvas. It should mention the three classes, the two relationships and the new constraint. If the description and the canvas disagree, the canvas is the truth: the description is generated text, the canvas is the model that generators read.
3. The :ui[Explain the specs] chip (shown after a model is created) sends a similar request for a plain-language overview.

:::checkpoint
The reply describes patients, doctors and appointments and how they relate, and nothing in it contradicts what you see on the canvas.
:::

## Add a state machine by chat

The assistant can add a diagram of another type to the same project. Here you model the lifecycle of an appointment.

1. Send:

```text
Create a state machine for the appointment lifecycle with the states Requested, Confirmed, Completed and Cancelled.
```

2. The assistant adds a state machine diagram and switches the canvas to it. Close the workspace and look at the :ui[State] editor in the left sidebar.
3. Check that the four states exist, that there is an initial state, and that the transitions make sense (for example Requested to Confirmed, Confirmed to Completed, and transitions to Cancelled). Transition names are chosen by the assistant and vary.
4. If a state is missing, ask for it by name, for example `Add a NoShow state to the state machine, reachable from Confirmed.`

<!-- TODO screenshot: the appointment state machine on the State canvas with Requested, Confirmed, Completed and Cancelled (appointment-state-machine.png). -->

:::note
The assistant supports eight of the nine diagram types: class, object, state machine, agent, user, GUI, quantum circuit and BPMN. Neural network diagrams are not supported, and the assistant button is hidden while a Neural Net diagram is open.
:::

:::checkpoint
The sidebar :ui[State] editor contains a state machine with the states Requested, Confirmed, Completed and Cancelled, and the :ui[Class] editor still contains your class diagram.
:::

## Validate the model and generate code from the chat

1. Click :ui[Class] in the left sidebar so the class diagram is active.
2. Click :ui[Quality Check] (the check-mark button in the top bar). Resolve any reported errors before you generate. A valid diagram shows "Diagram is valid". Quality Check validates the model; it says nothing about generated code.
3. Open the chat again and send:

```text
Generate SQL schema for PostgreSQL
```

4. The assistant runs the same SQL DDL generator as :ui[Generate > Database > SQL DDL], with the PostgreSQL dialect taken from your sentence, and your browser downloads the result. The deterministic generators need no API key and give the same output for the same model.
5. Open the downloaded file in a text editor. Check that it contains a `CREATE TABLE` statement for each class and a foreign key from the appointment table to the doctor table.

<!-- TODO screenshot: the assistant reply to "Generate SQL schema for PostgreSQL" after the download (assistant-sql-reply.png). -->

:::note
Other inline generator requests follow the same pattern, for example `generate django backend with project name "clinic" and app name "appointments"` or `generate python`. Requests for a whole application ("generate the web app") are different: they start the Spec-Driven Agent, which uses a language model to build an app on top of the generators. That is the subject of the [next lab](/labs/spec-driven-agent/).
:::

:::troubleshoot
**Nothing downloads, or the assistant replies with a list of generators ("What would you like me to generate? Here are the available options...").** The request was not recognised as a specific generator. Reply with the generator name it lists, for example `generate sql`, or use :ui[Generate > Database > SQL DDL] and pick :ui[PostgreSQL] in the dialog. If the browser blocked the download, allow downloads for the editor site.
:::

:::checkpoint
Quality Check reports the class diagram as valid, and you have a downloaded SQL file whose `CREATE TABLE` statements match the classes on the canvas.
:::

## Exercise: extend the clinic by conversation

:::exercise[Add prescriptions and keep the model consistent]
Using only the chat, add a `Prescription` class that belongs to exactly one appointment (an appointment can have several prescriptions), with a medication name and a dosage. Then add a constraint that a prescription's dosage must not be empty. Verify every change on the canvas, run Quality Check, and export the project with :ui[File > Export Project] as a JSON backup.
:::

:::solution
Two short prompts work better than one long one: first create the class and its association, then add the constraint. On the canvas, check that the association end on the Prescription side is many and on the Appointment side is `1`. A constraint such as `context Prescription inv: self.dosage <> ''` is one valid form.
:::

:::exercise[Compare chat and canvas]
Rebuild the same three-class clinic model by hand on the canvas in a second project, as in Lab 1. Export both projects as B-UML (:ui[File > Export Project], then :ui[Export as B-UML]) and compare the two Python files. Which differences come from the assistant's choices (names, types, multiplicities) and which are only layout?
:::

:::solution
Layout is not part of the B-UML export, so any difference you find in the files is a modeling decision. Typical differences are attribute types (`str` versus `date` for a date), an extra identifier attribute, and the role names on association ends.
:::
