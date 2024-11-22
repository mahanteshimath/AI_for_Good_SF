import streamlit as st
import snowflake.snowpark as snowpark
from snowflake.snowpark.session import Session
import pandas as pd

# Set pandas options
pd.set_option("max_colwidth", None)

# Default values for the chat assistant
num_chunks = 3
slide_window = 7

# Establish a Snowflake session using Snowpark
def get_snowflake_session():
    try:
        # Define your connection parameters
        connection_parameters = {
            "account": st.session_state.get("account"),
            "user": st.session_state.get("user"),
            "password": st.session_state.get("password"),
            "role": st.session_state.get("role"),
            "warehouse": st.session_state.get("warehouse"),
            "database": 'CC_QUICKSTART_CORTEX_DOCS',
            "schema": 'DATA',
        }

        # Create a new session
        session = Session.builder.configs(connection_parameters).create()
        return session
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return None

# Configuration options
def config_options():
    st.selectbox(
        'Select your model:',
        (
            'mixtral-8x7b', 'snowflake-arctic', 'mistral-large',
            'llama3-8b', 'llama3-70b', 'reka-flash', 
            'mistral-7b', 'llama2-70b-chat', 'gemma-7b'
        ), 
        key="model_name"
    )
    st.checkbox('Remember chat history?', key="debug", value=False)
    st.button("Start Over", key="clear_conversation")

# Initialize chat history
def init_messages():
    if st.session_state.get("clear_conversation") or "messages" not in st.session_state:
        st.session_state["messages"] = []

# Title and intro
st.title(":blue[📈 Analysis with Snowflake Cortex & RAG] :speech_balloon:")

# Initialize session state variables
if "model_name" not in st.session_state:
    st.session_state["model_name"] = 'mixtral-8x7b'  # Default model name

# Get active Snowflake session
session = get_snowflake_session()

if session is None:
    st.stop()

# Create columns for layout
col1, col2, col3 = st.columns([1, 0.05, 1])

with col1:
    st.write("### Configuration Options")
    config_options()

    # Add custom CSS to style the button
    st.markdown(
        """
        <style>
        .glowing-button {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 8px;
            box-shadow: 0 0 5px red, 0 0 10px red, 0 0 15px red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <style>
        .divider {
            height: 100%;
            width: 1px;
            background-color: #e0e0e0;
            margin: 0 10px;
        }
        </style>
        <div class="divider"></div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.write("### Documents Available")
    st.write("This is the list of documents you already have and that will be used to answer your questions:")

    # Query to list available documents
    try:
        docs_available = session.sql("LIST @docs").collect()
        list_docs = [doc["name"] for doc in docs_available]
        st.dataframe(list_docs)
    except Exception as e:
        st.error(f"Error fetching documents: {str(e)}")

st.divider()

init_messages()

# Display chat messages from history on app rerun
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to handle user input and generate responses
def handle_user_input():
    question = st.text_input("Ask a question:")
    if question:
        st.session_state.messages.append({"role": "user", "content": question})

        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(question)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            question = question.replace("'", "")
            with st.spinner(f"{st.session_state.model_name} thinking..."):
                response = complete(session, question)
                res_text = response[0].RESPONSE
                res_text = res_text.replace("'", "")
                message_placeholder.markdown(res_text)

        st.session_state.messages.append({"role": "assistant", "content": res_text})

handle_user_input()
