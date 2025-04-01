import pandas as pd
import streamlit as st

from agent_generation.generator.agent_generator import generate_agent


def generator_ui():
    st.header('Agent generator')
    with st.form('upload_data', clear_on_submit=True):
        st.subheader('Import a csv file')
        agent_name = st.text_input(label='Agent name', placeholder='Example: sales_agent')
        uploaded_file = st.file_uploader(label="Choose a file", type='csv')
        submitted = st.form_submit_button(label="Create agent", type='primary')
        if submitted:
            if uploaded_file is None:
                st.error('Please add a dataset')
            else:
                if agent_name is None or agent_name == '':
                    agent_name = uploaded_file.name[:-4]  # remove .csv file extension
                if agent_name in st.session_state['agent_manager'].agents:
                    st.error(f"The agent name '{agent_name}' already exists. Please choose another one")
                else:
                    with st.spinner('Generating the agent'):
                        agent = generate_agent(agent_name, pd.read_csv(uploaded_file))
                    if agent:
                        st.info(f'The agent **{agent.name}** has been created!')
                        with st.spinner('Training the agent'):
                            st.session_state['agent_manager'].add_agent(agent)
                            agent.run(sleep=False)
                        st.info(f'The agent **{agent.name}** is now running!')
                    else:
                        st.error('The agent was not generated')
