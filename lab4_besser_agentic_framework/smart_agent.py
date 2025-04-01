# You may need to add your working directory to the Python path. To do so, uncomment the following lines of code
# import sys
# sys.path.append("/Path/to/directory/agentic-framework") # Replace with your directory path
import base64
import io
import logging

import fitz  # pip install pymupdf
from besser.agent.core.file import File
from besser.agent.nlp import OPENAI_API_KEY
from besser.agent.nlp.intent_classifier.intent_classifier_configuration import LLMIntentClassifierConfiguration
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from besser.agent.core.agent import Agent
from besser.agent.core.session import Session
from besser.agent.exceptions.logger import logger
from besser.agent.nlp.llm.llm_openai_api import LLMOpenAI
from besser.agent.nlp.rag.rag import RAGMessage, RAG
from langchain.schema import Document

# Configure the logging module (optional)
logger.setLevel(logging.INFO)

# Create the agent
agent = Agent('rag_agent')
# Load agent properties stored in a dedicated file
agent.load_properties('config.ini')
agent.set_property(OPENAI_API_KEY, 'YOUR-API-KEY')
# Define the platform your agent will use
websocket_platform = agent.use_websocket_platform(use_ui=True)

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

ic_config = LLMIntentClassifierConfiguration(
    llm_name='gpt-4o-mini',
    parameters={},
    use_intent_descriptions=True,
    use_training_sentences=False,
    use_entity_descriptions=True,
    use_entity_synonyms=False
)
agent.set_default_ic_config(ic_config)


# STATES

initial_state = agent.new_state('initial_state', initial=True)
awaiting_state = agent.new_state('awaiting_state')


# STATES BODIES' DEFINITION + TRANSITIONS

def initial_body(session: Session):
    pass


initial_state.set_body(initial_body)
initial_state.go_to(awaiting_state)


def awaiting_body(session: Session):
    session.reply('Hi! What can I do for you?')


awaiting_state.set_body(awaiting_body)
awaiting_state.when_no_intent_matched_go_to(awaiting_state)  # REMOVE THIS TRANSITION ONCE YOU START DEVELOPING THE AGENT

# RUN APPLICATION

if __name__ == '__main__':
    agent.run()
