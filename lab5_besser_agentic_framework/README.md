# Lab 5 — Building Agents with BAF

## At a glance

- **You'll learn:** How to build intelligent agents with the [BESSER Agentic Framework](https://besser-agentic-framework.readthedocs.io/latest/) — covering state machines, LLM-backed intent classification, Retrieval-Augmented Generation (RAG), custom processors, and no-code agent generation from CSV.
- **You'll produce:** A RAG-powered chatbot in [`smart_agent.py`](smart_agent.py) and a Streamlit app that generates new agents from CSV data.
- **You'll need first:** No prior labs required — but familiarity with Python and basic state machines helps.

---

## Prerequisites

- **Python** 3.11+
- **BAF** installed with all extras:
  ```bash
  pip install besser-agentic-framework[all]
  ```
- An **OpenAI API key** (or equivalent for HuggingFace / Replicate if you prefer)
- `pip install pymupdf` for PDF loading (used in the RAG exercise)

**Install check** — run this to confirm BAF imports cleanly:

```python
from baf.core.agent import Agent

agent = Agent('test_agent')
print('BAF installed correctly. Agent created:', agent.name)
```

---

## 1. Context

The [BESSER Agentic Framework (BAF)](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework) is a Python library for building agents with **rule-based behaviors** augmented by **AI components** (LLMs, RAG, embeddings, NER). Agents in BAF are modeled as state machines: every user message is evaluated against outgoing transitions from the current state, the agent moves to the next state, and that state's body runs.

This lab has three distinct parts:

| Part | What you build | Approach |
|---|---|---|
| **Low-code agent** (section 3) | A chatbot powered by RAG + LLM in `smart_agent.py` | You write the Python directly |
| **No-code agent generator** (section 4) | A Streamlit app that generates agents from CSV | You implement a template filler |
| **Custom processor** (section 5) | A message processor plugged into an agent | You subclass `Processor` |

Useful references:

- [BAF documentation](https://besser-agentic-framework.readthedocs.io/latest/)
- [BAF source code](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework)

---

## 2. Scenario

You will build a **RAG-powered assistant** that can answer questions grounded in documents you upload. The final state machine looks like this:

<div align="center">
  <img src="figs/smart_agent.png" alt="Agent state machine" width="600"/>
</div>

The agent has four interactive states beyond the initial state:

- **`awaiting_state`** — the hub, waiting for user input
- **`load_document_state`** — stores uploaded PDFs into a vector store
- **`rag_state`** — answers questions using retrieved document chunks
- **`llm_state`** — handles instructions with a plain LLM call (no retrieval)

---

## 3. Walkthrough — Low-code agent

### 3.1 Starter file

Open [`smart_agent.py`](smart_agent.py). It already contains the imports, config loading, and two empty states (`initial_state` and `awaiting_state`). You will extend it step by step.

```python
agent = Agent('rag_agent')
agent.load_properties('config.yaml')
websocket_platform = agent.use_websocket_platform(use_ui=True)
```

Your OpenAI key lives in [`config.yaml`](config.yaml) under `nlp.openai.api_key`. Alternatively, set it in code:

```python
# option 1 (recommended) — from config.yaml
agent.load_properties('config.yaml')
# option 2 — inline
agent.set_property(OPENAI_API_KEY, 'YOUR-API-KEY')
```

### 3.2 Configure the LLM

Instantiate an OpenAI LLM. You can swap in HuggingFace or Replicate with the same pattern — see the commented alternatives in `smart_agent.py`.

```python
gpt = LLMOpenAI(
    agent=agent,
    name='gpt-4o-mini',
    parameters={},
    num_previous_messages=0,
)
```

> **Tip:** You can create a free HuggingFace account and use LLMs through its Inference API. Note the available models are limited and quota-capped.

### 3.3 Configure the intent classifier

BAF supports two intent classifiers: a simple neural network and an LLM-based one. LLM classification generally works better:

```python
ic_config = LLMIntentClassifierConfiguration(
    llm_name='gpt-4o-mini',
    parameters={},
    use_intent_descriptions=True,
    use_training_sentences=False,
    use_entity_descriptions=True,
    use_entity_synonyms=False,
)
agent.set_default_ic_config(ic_config)
```

Run the agent. At this point only `initial_state` and `awaiting_state` are wired — the agent will reply but can't do much yet.

### 3.4 Create the RAG component

RAG (Retrieval-Augmented Generation) combines a **vector store** of document chunks with an LLM: given a query, the retriever fetches the top-k most relevant chunks, and the LLM generates an answer grounded in them.

BAF's RAG takes three inputs: an LLM (already created), a text splitter, and a vector store.

```python
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from baf.nlp.rag.rag import RAGMessage, RAG

embeddings = OpenAIEmbeddings(openai_api_key='api-key')

vector_store: Chroma = Chroma(
    embedding_function=embeddings,
    persist_directory='vector_store',  # optional persistence directory
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

rag = RAG(
    agent=agent,
    vector_store=vector_store,
    splitter=splitter,
    llm_name='gpt-4o-mini',
    k=4,                    # number of chunks to retrieve
    num_previous_messages=0,  # previous messages to add to the query
)
```

### 3.5 Add document loading

Create a new state `load_document_state`. Add a transition from `awaiting_state` triggered when the user uploads a PDF ([file transitions docs](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/transitions.html#file-transitions)):

```python
awaiting_state.when_file_received(allowed_types='application/pdf').go_to(load_document_state)
```

State body:

```python
def load_document_body(session: Session):
    file: File = session.event.file
    load_pdf_from_base64(file, rag)
    session.reply('Document loaded!')

load_document_state.set_body(load_document_body)
load_document_state.go_to(awaiting_state)
```

Helper function to convert a base64-encoded PDF into vector-store chunks:

```python
def load_pdf_from_base64(file: File, rag: RAG):
    pdf_bytes = base64.b64decode(file.base64)
    pdf_file = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    documents = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        documents.append(Document(
            page_content=text,
            metadata={"page": page_num, "source": file.name},
        ))
    chunked_documents = rag.splitter.split_documents(documents)
    n_chunks = len(chunked_documents)
    rag.vector_store.add_documents(chunked_documents)
    logger.info(f'[RAG] Added {n_chunks} chunks. Total: {len(rag.vector_store.get()["documents"])}')
```

Run the agent and upload a short scientific paper to test the loader.

> **Tip:** Uploading the same file twice creates duplicate chunks. Delete the `vector_store/` folder between runs if you want a clean slate.

### 3.6 Add the RAG state

Create an intent that matches questions:

```python
question_intent = agent.new_intent(
    'question_intent',
    description='The message is a question, finishing with a question mark (?)',
)
```

Now define `rag_state` and the transition from `awaiting_state` ([intent transitions docs](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/transitions.html#intent-transitions)):

```python
def rag_body(session: Session):
    rag_message: RAGMessage = session.run_rag(session.event.message)
    # You can save the answer in the session if you want it for later
    websocket_platform.reply_rag(session, rag_message)

rag_state.set_body(rag_body)
rag_state.go_to(awaiting_state)
```

Run the agent and ask questions about your uploaded document.

### 3.7 Add the LLM state

For non-question inputs (instructions, commands), route to a plain LLM call:

```python
instruction_intent = agent.new_intent(
    'instruction_intent',
    description='The message is an instruction. Do not consider questions as instructions.',
)

def llm_body(session: Session):
    # Optionally prepend instructions: "You are an expert in X", "You are talking to a kid"
    answer = gpt.predict(session.event.message)
    session.reply(answer)

llm_state.set_body(llm_body)
llm_state.go_to(awaiting_state)
```

You now have a full agent: questions go to RAG, instructions go to the LLM, file uploads are indexed.

---

## 4. Walkthrough — No-code agent generator

In the previous section you wrote the agent manually. In this section you will generate one **automatically from a CSV file** — a no-code approach.

The [`agent_generation/`](agent_generation) package contains a Streamlit app that lets you upload a CSV and creates an agent script from it.

### 4.1 Run the app

```bash
streamlit run agent_generation.py
```

> Streamlit auto-reloads on file changes — just refresh the browser to pick up your edits.

Upload a CSV using [`sample_data.csv`](agent_generation/sample_data.csv) as reference. The CSV format is two columns — `question` and `answer` — where multiple questions can share the same answer (some rows in the sample have empty answers precisely because they are alternative phrasings for the previous answer).

### 4.2 Your task

Implement `generate_agent()` in [`agent_generation/generator/agent_generator.py`](agent_generation/generator/agent_generator.py). It runs every time you click the **Create agent** button and receives two arguments: the agent name and the pandas `DataFrame` from the CSV.

Your implementation should:

1. Build a Python dictionary (`data`) containing the information needed to generate an agent script (e.g. a list of intents and a list of states, one per unique answer).
2. Render the Jinja template [`agent_generation/generator/agent_generation.py.j2`](agent_generation/generator/agent_generation.py.j2) with that dictionary.
3. Write the rendered Python file to `agent_generation/agents/<agent_name>.py`.

The generated agent must have a **central state** that receives all user questions and one **answer state** per unique answer in the CSV. When a question matches an intent, the agent transitions to the corresponding answer state, replies, and returns to the central state.

### 4.3 Jinja tips

Example data structure to pass into the template:

```python
data = {
    'elements': [
        {'name': 'e1', 'value': True},
    ],
}
```

Loop:

```jinja
{% for element in elements %}
 Your code here
{% endfor %}
```

Access fields:

```jinja
{{ element.name }}
```

Generated agent scripts are stored under [`agent_generation/agents/`](agent_generation/agents).

---

## 5. Walkthrough — Custom processor

A [processor](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/processors.html) intercepts user and/or agent messages for side-effects: language detection, sentiment analysis, translation, style adaptation, etc. BAF ships two example processors:

- [Language detection](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework/blob/main/baf/core/processors/language_detection_processor.py)
- [User adaptation](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework/blob/main/baf/core/processors/user_adaptation_processor.py) (LLM-based)

**Your task**: build a custom processor and plug it into your agent.

Ideas:

- **Sentiment analysis** — tag each user message as `positive`, `neutral`, or `negative`
- **Translator** — translate user or agent messages to a target language
- **Internet slang normalizer** — `idk who r u` → `I don't know who you are`

---

## 6. Exercises

> **Exercise 6.1 — Run the full RAG agent**
>
> Complete all seven sub-steps in section 3. Upload a short scientific paper, then ask 3 questions and send 1 instruction. Verify the agent routes each to the correct state.

> **Exercise 6.2 — Implement the agent generator**
>
> Implement `generate_agent()` and the Jinja template from section 4. Test by generating an agent from `sample_data.csv` and running it from the app.

> **Exercise 6.3 — Build one custom processor**
>
> Pick one of the ideas from section 5 (or invent your own). Implement it, attach it to your RAG agent, and verify it fires on the user messages.

---

## 7. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `ModuleNotFoundError: No module named 'baf'` | BAF version too old (≤4.2.x) | Upgrade: `pip install --upgrade "besser-agentic-framework[all]"` — the package was renamed `besser.agent` → `baf` in 4.3.x |
| `ValueError: Only YAML configuration files are supported (.yaml, .yml)` | Your config file is `.ini` | Convert to `config.yaml` — BAF dropped `.ini` support in 4.3.x |
| `AttributeError: 'Session' object has no attribute 'message'` / `'file'` | Using the old event API | BAF now exposes the event via `session.event.*`: use `session.event.message` and `session.event.file` |
| `openai.AuthenticationError` | OpenAI key missing or wrong | Check `config.yaml` → `nlp.openai.api_key` or set it inline |
| RAG returns unrelated chunks | Vector store not empty from an earlier run | Delete the `vector_store/` folder and re-upload the document |
| Streamlit doesn't pick up code changes | Hot-reload stale | Refresh the browser tab (Ctrl+R) |
| `ModuleNotFoundError: No module named 'fitz'` | `pymupdf` missing | `pip install pymupdf` |
| HuggingFace property error | BAF renamed `HF_API_KEY` → `HF_TOKEN` (`nlp.hf.api_key` → `nlp.huggingface.token`) | Update `config.yaml` accordingly |

---

## 8. What's next

Head to **[Lab 6 — From Modeling to Deployment](../lab6_render_deployment/README.md)** to combine everything you've built so far — class diagrams, agents, and GUI models — into a full web application deployed on Render.

---

## Resources

- [BAF documentation](https://besser-agentic-framework.readthedocs.io/latest/)
- [BAF source code](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework)
- [RAG guide](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/rag.html)
- [LLM guide](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/llm.html)
- [Intent classification](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/intent_classification.html)
- [WebSocket platform](https://besser-agentic-framework.readthedocs.io/latest/wiki/platforms/websocket_platform.html)
- [Transitions reference](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/transitions.html)
- [Processors reference](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/processors.html)
