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

# Get similar chunks based on the question
def get_similar_chunks(session, question):
    cmd = """
    WITH results AS (
        SELECT RELATIVE_PATH,
               VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
               SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', ?)) AS similarity,
               chunk
        FROM docs_chunks_table
        ORDER BY similarity DESC
        LIMIT ?
    )
    SELECT chunk, relative_path FROM results
    """
    df_chunks = session.sql(cmd, params=[question, num_chunks]).to_pandas()
    similar_chunks = " ".join(df_chunks['CHUNK'].tolist())
    return similar_chunks.replace("'", "")

# Create the final prompt
def create_prompt(session, myquestion):
    prompt_context = get_similar_chunks(session, myquestion)
    chat_history = st.session_state.get("messages", [])
    prompt = f"""
    <context>{prompt_context}</context>
    <question>{myquestion}</question>
    """
    return prompt

# Send prompt to Snowflake Cortex for completion
def complete(session, myquestion):
    prompt = create_prompt(session, myquestion)
    cmd = "SELECT SNOWFLAKE.CORTEX.COMPLETE(?, ?) AS RESPONSE"
    df_response = session.sql(cmd, params=[st.session_state.model_name, prompt]).collect()
    return df_response

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
            transition: box-shadow 0.3s ease-in-out;
        }
        .glowing-button:hover {
            box-shadow: 0 0 20px red, 0 0 30px red, 0 0 40px red;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# Initialize chat history
init_messages()

# Display chat messages from history on app rerun
for message in st.session_state.get("messages", []):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input for questions
if question := st.chat_input("Chat with any docs"):
    # Add user message to chat history
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

# Footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #2C1E5B;
        color: white;
        text-align: center;
    }
    </style>
    <div class="footer">
    <p>Developed with ❤️ by <a href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">Mahantesh Hiremath</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
