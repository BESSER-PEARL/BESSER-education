# Lab Guide 4: Building agents with BESSER Agentic Framework

## Welcome to our BESSER lab guide!

In this guide, you will use [BESSER Agentic Framework](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework) (BAF)
to design smart agents.

BAF is a Python library with which you can design agents with rule-based behaviours but also take advantage of AI components like LLMs.

[BAF Documentation](https://besser-agentic-framework.readthedocs.io/latest/)
[BAF Code](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework)

## 1. Requirements

Follow the instructions in the [documentation](https://besser-agentic-framework.readthedocs.io/latest/) to install BAF.
You will need to add the options [extras,llms,pytorch]

You can check if the installation was properly done by running an example agent in the BAF library. You can try to run the Greetings Agent:

```python
from baf.test.examples.greetings_agent import agent

agent.run()
```

## 2. No-code agent development

In this exercise we will create an agent without writing any code, just by using the BESSER Web Modeling Editor.

https://editor.besser-pearl.org/

We will create an agent that can query a SQL database using Natural Language.

Go to the agent diagram editor and load the template agent **Database Agent**

Once you have loaded the agent model, we can export the actual Agent Python code.

For this exercise, we will use this Database: https://github.com/lerocha/chinook-database

Go to Releases and downlaod the latest .sqlite file.

Then, go to the config.yaml file and add the path to the database (under the section db.sql)

At this point, you can run and test the agent.

The generated agent uses the LLM to generate an answer from the retrieved data from the database. We can modify it so that the agent answer is only the sql data without any LLM processing.
To do so, we will add this function to our agent:

```python
import pandas as pd

def to_dataframe(result):
    if result is None:
        return None

    # Multiple rows
    if isinstance(result, list):
        return pd.DataFrame(result)

    # Single row (dict)
    if isinstance(result, dict):
        return pd.DataFrame([result])

    # Scalar value
    return pd.DataFrame([{"value": result}])

```

This will parse our SQL result into a Pandas Dataframe.
The last step is to change the type of reply of the agent to a Dataframe reply.


## 3. Low-code agent development

In this exercise we will create an agent powered by [RAG](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/rag.html)
and an [LLM](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/llm.html). This is how the agent's state machine will look like:

<div align="center">
  <img src="figs/rag_agent.png" alt="Agent state machine" width="600"/>
</div>

In [rag_agent.py](rag_agent.py), you will write the agent code. This file already contains some code to import the necessary classes and create the agent.

```python
agent = Agent('rag_agent')
```

You will need an OpenAI API key. You can store it in a dedicated `config.ini` file, or define it directly in the code:

```python
# option 1
agent.load_properties('config.ini')
# option 2
agent.set_property(OPENAI_API_KEY, 'YOUR-API-KEY')
```

The agent will use the [WebSocket](https://besser-agentic-framework.readthedocs.io/latest/wiki/platforms/websocket_platform.html)
platform to receive and send messages.

```python
websocket_platform = agent.use_websocket_platform(use_ui=True)
```

Next, we want to instantiate the LLM we will use. In this case, an OpenAI LLM, although you can also use other providers, such as HuggingFace.

> You can create a free HuggingFace account and use LLMs through its InferenceAPI. Note that limited models are available and with quota limits. 

```python
gpt = LLMOpenAI(
    agent=agent,
    name='gpt-4o-mini',
    parameters={},
    num_previous_messages=0
)

# Other example LLMs

# gemma = LLMHuggingFace(agent=agent, name='google/gemma-2b-it', parameters={'max_new_tokens': 1}, num_previous_messages=10)
# llama = LLMHuggingFaceAPI(agent=agent, name='meta-llama/Meta-Llama-3.1-8B-Instruct', parameters={}, num_previous_messages=10)
# mixtral = LLMReplicate(agent=agent, name='mistralai/mixtral-8x7b-instruct-v0.1', parameters={}, num_previous_messages=10)
```

Next, we will configure the agent's [intent classifier](https://besser-agentic-framework.readthedocs.io/latest/wiki/nlp/intent_classification.html).
We can use either a simple neural network performing a typical text classification task, or we can use an LLM, wich generally works better. This is the configuration we will use in this agent:

```python
ic_config = LLMIntentClassifierConfiguration(
    llm_name='gpt-4o-mini',
    parameters={},
    use_intent_descriptions=True,
    use_training_sentences=False,
    use_entity_descriptions=True,
    use_entity_synonyms=False
)
agent.set_default_ic_config(ic_config)  # Note: We can configure the intent classifier for each individual state if we want
```

Try to run the agent. At this point, there is only the initial state and the awaiting state. The initial state is usually defined to perform some initialization if necessary. For now, this state will not do any task.

### Retrieval Augmented Generation (RAG)

We will implement 2 states for RAG. One, will be used to store pdf files into our vector store, and the other to generate RAG-based answers.

#### Create the RAG

First, we need to create the RAG component of the agent. RAG requires 3 elements: an LLM, a text splitter (which will split our documents in smaller chunks) and a vector store (the database that will store the vectorized representations of the chunks)

```python
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from baf.nlp.rag.rag import RAGMessage, RAG

embeddings = OpenAIEmbeddings(openai_api_key='api-key')


vector_store: Chroma = Chroma(
    embedding_function=embeddings,
    persist_directory='vector_store'  # directory where we store the vector store, optional
)

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


rag = RAG(
    agent=agent,
    vector_store=vector_store,
    splitter=splitter,
    llm_name='gpt-4o-mini',
    k=4,  # Number of chunks to retrieve
    num_previous_messages=0  # Number of previous messages to add to the query
)
```

#### Load documents

Create a state called `load_document_state`. You need to define the transition from `awaiting_state` to `load_document_state`. This transition has
to be triggered when a file is received.

(more info: https://besser-agentic-framework.readthedocs.io/latest/wiki/core/transitions.html#file-transitions)

```python
awaiting_state.when_file_received_go_to(load_document_state, allowed_types='application/pdf')
```

Next, we need to implement the body of `load_document_state`:

```python
def load_document_body(session: Session):
    file: File = session.file
    load_pdf_from_base64(file, rag)
    session.reply('Document loaded!')

load_document_state.set_body(load_document_body)
load_document_state.go_to(awaiting_state)
```

You can use the following auxiliar function to help you load the documents into the vector store:

(You will need to install `pip install pymupdf`)

```python
def load_pdf_from_base64(file: File, rag: RAG):
    pdf_bytes = base64.b64decode(file.base64)
    pdf_file = io.BytesIO(pdf_bytes)
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    documents = []
    for page_num in range(len(doc)):
        text = doc[page_num].get_text("text")
        documents.append(Document(page_content=text, metadata={"page": page_num, "source": file.name}))
    chunked_documents = rag.splitter.split_documents(documents)
    n_chunks = len(chunked_documents)
    rag.vector_store.add_documents(chunked_documents)
    logger.info(f'[RAG] Added {n_chunks} chunks to RAG\'s vector store. Total: {len(rag.vector_store.get()["documents"])}')
```

Take a moment to run the agent and check if the document loading functionality works correctly. Note that if you upload 2 
times the same document, the vector store will contain duplicate chunks! You can always remove the vector store and start again 
(i.e., remove the `vector_store` folder that has been created).

You can try uploading a scientific paper. It is a relatively short document that you can use for question answering later with RAG.

#### RAG State

Now we need the RAG state, which will use our vector store to retrieve relevant chunks of documents to help the LLM generate context-aware answers

Create a state called `rag_state`. Create an intent called `question_intent` with a description like this:

```python
question_intent = agent.new_intent('question_intent', description='The message is a question, finishing with a question mark (?)')
```

The LLM-based intent classifier can use intent descriptions to try to assign the correct intent to the user messages. This intent will be matched whenever
a user message is a question.

Now, we need to define the transition from `awaiting_state` to `rag_state` when the `question_intent` is matched from the user input.

Check the documentation to see how to create intent-based transitions: https://besser-agentic-framework.readthedocs.io/latest/wiki/core/transitions.html#intent-transitions

Now, we will define the body of the `rag_state`

```python
def rag_body(session: Session):
    rag_message: RAGMessage = session.run_rag(session.message)
    # You can save the answer in the session if you want it for later
    websocket_platform.reply_rag(session, rag_message)


rag_state.set_body(rag_body)
rag_state.go_to(awaiting_state)
```

Try running the agent. Ask some question about the document (or documents) you uploaded.

### LLM

Now, we will create a state where we will use the LLM to perform some tasks. We will create an intent called `instruction_intent` that will be used to transition to the LLM state, as shown in the agent diagram above.

```python
instruction_intent = agent.new_intent('instruction_intent', description='The message is an instruction. Do not consider questions as instructions.')
```

This way, when a question is sent, the agent will run RAG, while when the message is an instruction, only the LLM will be used.

```python
def llm_body(session: Session):
    # You can add some instructions together with the message to adapt the LLM message (e.g., "You are an expert in...", "You are talking to a kid...", etc.)
    answer = gpt.predict(session.message)
    session.reply(answer)


llm_state.set_body(llm_body)
llm_state.go_to(awaiting_state)
```

At this point, you can run the agent to test all the functionalities we implemented! Feel free to extend it for other tasks!

## 4. Implementing a custom language processor

A [processor](https://besser-agentic-framework.readthedocs.io/latest/wiki/core/processors.html) can be used to process user and/or agent messages for specific purposes.
BAF comes with 2 example processors to (1) [detect the message language](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework/blob/v2.1.0/besser/agent/core/processors/language_detection_processor.py)
and (2) [adapt the agent messages to specific user profiles](https://github.com/BESSER-PEARL/BESSER-Agentic-Framework/blob/v2.1.0/besser/agent/core/processors/user_adaptation_processor.py) (this one using an LLM).

In this exercise, you will create a custom processor for your agent. Read the processors documentation and the existing processors to understand how to create it. Here you have some ideas for processors:

- Sentiment Analysis: recognize the sentiment of a user message (e.g., "positive", "neutral" or "negative").
- Translator: translate user/agent messages to a target language.
- Internet slang parsing: detect slang terms and covert them into standard text (e.g. from "idk who r u" to "I don't know who are you")
