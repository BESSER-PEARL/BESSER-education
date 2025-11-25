import base64
import json
import queue
import threading
from datetime import datetime
from io import StringIO

import cv2
import numpy as np
import pandas as pd
import plotly
import streamlit as st
import websocket
from besser.agent.core.agent import Agent
from besser.agent.platforms.websocket import WEBSOCKET_HOST, WEBSOCKET_PORT
from besser.agent.platforms.websocket.streamlit_ui.chat import write_message
from besser.agent.platforms.websocket.streamlit_ui.vars import *
from streamlit.runtime import Runtime
from streamlit.runtime.app_session import AppSession
from streamlit.runtime.scriptrunner import add_script_run_ctx, get_script_run_ctx

from besser.agent.platforms.payload import Payload, PayloadAction, PayloadEncoder
from besser.agent.core.message import Message, MessageType

# Time interval to check if a streamlit session is still active, in seconds
SESSION_MONITORING_INTERVAL = 10


def get_streamlit_session() -> AppSession or None:
    session_id = get_script_run_ctx().session_id
    runtime: Runtime = Runtime.instance()
    return next((
        s.session
        for s in runtime._session_mgr.list_sessions()
        if s.session.id == session_id
    ), None)


def agent_ui(agent: Agent):
    st.header(agent.name)
    # User input component. Must be declared before history writing

    def on_message(ws, payload_str):
        # https://github.com/streamlit/streamlit/issues/2838
        streamlit_session = get_streamlit_session()
        payload: Payload = Payload.decode(payload_str)
        content = None
        if payload.action == PayloadAction.AGENT_REPLY_STR.value:
            content = payload.message
            t = MessageType.STR
        elif payload.action == PayloadAction.AGENT_REPLY_MARKDOWN.value:
            content = payload.message
            t = MessageType.MARKDOWN
        elif payload.action == PayloadAction.AGENT_REPLY_HTML.value:
            content = payload.message
            t = MessageType.HTML
        elif payload.action == PayloadAction.AGENT_REPLY_FILE.value:
            content = payload.message
            t = MessageType.FILE
        elif payload.action == PayloadAction.AGENT_REPLY_IMAGE.value:
            decoded_data = base64.b64decode(payload.message)  # Decode base64 back to bytes
            np_data = np.frombuffer(decoded_data, np.uint8)  # Convert bytes to numpy array
            img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)  # Decode numpy array back to image
            content = img
            t = MessageType.IMAGE
        elif payload.action == PayloadAction.AGENT_REPLY_DF.value:
            content = pd.read_json(StringIO(payload.message))
            t = MessageType.DATAFRAME
        elif payload.action == PayloadAction.AGENT_REPLY_PLOTLY.value:
            content = plotly.io.from_json(payload.message)
            t = MessageType.PLOTLY
        elif payload.action == PayloadAction.AGENT_REPLY_LOCATION.value:
            content = {
                'latitude': [payload.message['latitude']],
                'longitude': [payload.message['longitude']]
            }
            t = MessageType.LOCATION
        elif payload.action == PayloadAction.AGENT_REPLY_OPTIONS.value:
            t = MessageType.OPTIONS
            d = json.loads(payload.message)
            content = []
            for button in d.values():
                content.append(button)
        elif payload.action == PayloadAction.AGENT_REPLY_RAG.value:
            t = MessageType.RAG_ANSWER
            content = payload.message
        if content is not None:
            message = Message(t=t, content=content, is_user=False, timestamp=datetime.now())
            streamlit_session._session_state[QUEUE].put(message)

        streamlit_session._handle_rerun_script_request()

    def on_error(ws, error):
        pass

    def on_open(ws):
        pass

    def on_close(ws, close_status_code, close_msg):
        pass

    def on_ping(ws, data):
        pass

    def on_pong(ws, data):
        pass

    user_type = {
        0: 'assistant',
        1: 'user'
    }

    if SUBMIT_TEXT not in st.session_state:
        st.session_state[SUBMIT_TEXT] = False

    if HISTORY not in st.session_state:
        st.session_state[HISTORY] = {}
    if agent.name not in st.session_state[HISTORY]:
        st.session_state[HISTORY][agent.name] = []

    if QUEUE not in st.session_state:
        st.session_state[QUEUE] = queue.Queue()

    if 'websockets' not in st.session_state:
        st.session_state['websockets'] = {}
    if agent.name not in st.session_state['websockets']:
        ws = websocket.WebSocketApp(f"ws://{agent.get_property(WEBSOCKET_HOST)}:{agent.get_property(WEBSOCKET_PORT)}/",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close,
                                    on_ping=on_ping,
                                    on_pong=on_pong)
        websocket_thread = threading.Thread(target=ws.run_forever)
        add_script_run_ctx(websocket_thread)
        websocket_thread.start()
        st.session_state['websockets'][agent.name] = ws

    ws = st.session_state['websockets'][agent.name]

    with st.sidebar:

        if reset_button := st.button(label="Reset agent"):
            st.session_state[HISTORY][agent.name] = []
            st.session_state[QUEUE] = queue.Queue()
            payload = Payload(action=PayloadAction.RESET)
            ws.send(json.dumps(payload, cls=PayloadEncoder))

    key_count = 0
    for message in st.session_state[HISTORY][agent.name]:
        write_message(message, key_count, stream=False)
        key_count += 1

    while not st.session_state[QUEUE].empty():
        message = st.session_state[QUEUE].get()
        st.session_state[HISTORY][agent.name].append(message)
        write_message(message, key_count, stream=True)
        key_count += 1

    if BUTTONS in st.session_state:
        buttons = st.session_state[BUTTONS]
        cols = st.columns(1)
        for i, option in enumerate(buttons):
            if cols[0].button(option):
                with st.chat_message("user"):
                    st.write(option)
                message = Message(t=MessageType.STR, content=option, is_user=True, timestamp=datetime.now())
                st.session_state['history'][agent.name].append(message)
                payload = Payload(action=PayloadAction.USER_MESSAGE,
                                  message=option)
                ws.send(json.dumps(payload, cls=PayloadEncoder))
                del st.session_state[BUTTONS]
                break

    def submit_text():
        # Necessary callback due to buf after 1.27.0 (https://github.com/streamlit/streamlit/issues/7629)
        # It was fixed for rerun but with _handle_rerun_script_request it doesn't work
        st.session_state[SUBMIT_TEXT] = True

    user_input = st.chat_input("What is up?", on_submit=submit_text)
    if st.session_state[SUBMIT_TEXT]:
        st.session_state[SUBMIT_TEXT] = False
        if BUTTONS in st.session_state:
            del st.session_state[BUTTONS]
        with st.chat_message(USER):
            st.write(user_input)
        message = Message(t=MessageType.STR, content=user_input, is_user=True, timestamp=datetime.now())
        st.session_state[HISTORY][agent.name].append(message)
        payload = Payload(action=PayloadAction.USER_MESSAGE,
                          message=user_input)
        try:
            ws.send(json.dumps(payload, cls=PayloadEncoder))
        except Exception as e:
            st.error('Your message could not be sent. The connection is already closed')

    st.stop()
