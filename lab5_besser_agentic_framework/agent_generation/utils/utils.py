import streamlit as st


def agent_selection():
    """Show an agent selection container"""
    st.subheader('Select an agent')
    selected_agent = st.selectbox(
        label='Select an agent',
        options=[agent_name for agent_name in st.session_state['agent_manager'].agents.keys()],
        label_visibility='collapsed',
    )
    if selected_agent:
        return st.session_state['agent_manager'].agents[selected_agent]
    else:
        return None
