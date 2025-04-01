import importlib

import numpy as np
import streamlit as st

from pandas import DataFrame

from jinja2 import Environment, FileSystemLoader


def generate_agent(agent_name: str, df: DataFrame):
    st.subheader('Data preview')
    st.dataframe(df)
    # EXERCISE

    data = {}

    ##################
    # YOUR CODE HERE #
    ##################

    env = Environment(loader=FileSystemLoader(''))
    template = env.get_template('agent_generation/generator/agent_generation.py.j2')
    rendered_code = template.render(data)
    with open(f'agent_generation/agents/{agent_name}.py', 'w') as file:
        file.write(rendered_code)

    gen_module = importlib.import_module(f'agent_generation.agents.{agent_name}')
    return gen_module.agent
