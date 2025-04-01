import streamlit as st
import sys
from streamlit.web import cli as stcli

from agent_generation.generator.agent_manager import AgentManager
from agent_generation.ui.agent_ui import agent_ui
from agent_generation.ui.generator_ui import generator_ui
from agent_generation.ui.sidebar import sidebar_menu
from agent_generation.utils.utils import agent_selection

st.set_page_config(layout="wide")

if __name__ == "__main__":
    if st.runtime.exists():
        if 'agent_manager' not in st.session_state:
            st.session_state['agent_manager'] = AgentManager()
        with st.sidebar:
            page = sidebar_menu()
        if page == 'Generator':
            generator_ui()
        elif page == 'Agents':
            with st.sidebar:
                agent = agent_selection()
            if agent:
                agent_ui(agent)
            else:
                st.info('Go to the Generator tab to create an agent')
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())
