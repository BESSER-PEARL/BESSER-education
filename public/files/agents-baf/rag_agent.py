# Starter for the BESSER Labs "agents-baf" lab (BAF 4.5.x).
# Run it from the folder that contains config.yaml:  python rag_agent.py
import logging

from baf import nlp
from baf.core.agent import Agent
from baf.core.session import Session
from baf.exceptions.logger import logger
from baf.nlp.intent_classifier.intent_classifier_configuration import LLMIntentClassifierConfiguration
from baf.nlp.llm.llm_openai_api import LLMOpenAI

# Show INFO logs in the terminal (optional)
logger.setLevel(logging.INFO)

# Create the agent and load config.yaml (your OpenAI key is in nlp.openai.api_key)
agent = Agent('rag_agent')
agent.load_properties('config.yaml')

# WebSocket platform; use_ui=True also starts the Streamlit chat page on http://localhost:5000
websocket_platform = agent.use_websocket_platform(use_ui=True)

# The LLM used for intent classification, RAG answers and the LLM state
gpt = LLMOpenAI(
    agent=agent,
    name='gpt-4o-mini',
    parameters={},
    num_previous_messages=0
)

# Classify user messages with the LLM, using the intent descriptions
ic_config = LLMIntentClassifierConfiguration(
    llm_name='gpt-4o-mini',
    parameters={},
    use_intent_descriptions=True,
    use_training_sentences=False,
    use_entity_descriptions=True,
    use_entity_synonyms=False
)
agent.set_default_ic_config(ic_config)

# TODO: splitter, vector store and RAG go here

# STATES

initial_state = agent.new_state('initial_state', initial=True)
awaiting_state = agent.new_state('awaiting_state')

# TODO: create load_document_state, rag_state and llm_state

# INTENTS

# TODO: create question_intent and instruction_intent

# STATE BODIES AND TRANSITIONS


def initial_body(session: Session):
    pass


initial_state.set_body(initial_body)
initial_state.go_to(awaiting_state)


def awaiting_body(session: Session):
    session.reply('Hi! Upload a PDF, ask me a question about it, or give me an instruction.')


awaiting_state.set_body(awaiting_body)
# Fallback: stay in awaiting_state when no intent matches. Add your transitions above this line.
awaiting_state.when_no_intent_matched().go_to(awaiting_state)

# RUN THE AGENT

if __name__ == '__main__':
    agent.run()
