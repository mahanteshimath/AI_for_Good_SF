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
            "account":st.session_state.account,
            "user": st.session_state.user,
            "password": st.session_state.password,
            "role": st.session_state.role,
            "warehouse": st.session_state.warehouse,
            "database": 'CC_QUICKSTART_CORTEX_DOCS',
            "schema": 'DATA',
        }

        # Create a new session
        session = Session.builder.configs(connection_parameters).create()
        return session
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
        return None

# Title and intro
st.title(":blue[📈Analysis with Snowflake Cortex & RAG ] :speech_balloon:")

# Get active Snowflake session
session = get_snowflake_session()

if session is None:
    st.stop()

# Create columns for layout
col1, col2, col3 = st.columns([1, 0.05, 1])

with col1:
    st.write("### Configuration Options")
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
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create a button using Streamlit
    if st.button("How RAG works in Snowflake?", key="rag_button", type="secondary"):
        show_dialog()

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
    docs_available = session.sql("ls @docs").collect()
    list_docs = []
    for doc in docs_available:
        list_docs.append(doc["name"])
    st.dataframe(list_docs)

st.divider()

# Initialize chat history
def init_messages():
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []

init_messages()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
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

# Configuration options
st.checkbox('Use chat history for context', key="use_chat_history", value=True)

# Debug option
st.checkbox('Debug: Click to see summary generated of previous conversation', key="debug", value=True)

# Button to start a new conversation
st.button("Start Over", key="clear_conversation")

# Show session state
# st.expander("Session State").write(st.session_state)

# Get similar chunks based on the question
def get_similar_chunks(session, question):
    cmd = """
    WITH results AS (
        SELECT RELATIVE_PATH,
        VECTOR_COSINE_SIMILARITY(docs_chunks_table.chunk_vec,
        SNOWFLAKE.CORTEX.EMBED_TEXT_768('e5-base-v2', ?)) AS similarity
        FROM docs_chunks_table
        ORDER BY similarity DESC
        LIMIT ?
    )
    SELECT chunk, relative_path FROM results
    """
    df_chunks = session.sql(cmd, params=[question, num_chunks]).to_pandas()
    similar_chunks = " ".join(df_chunks['CHUNK'].tolist())
    return similar_chunks.replace("'", "")

# Get chat history based on the slide window
def get_chat_history():
    chat_history = []
    start_index = max(0, len(st.session_state.messages) - slide_window)
    for i in range(start_index, len(st.session_state.messages) - 1):
        chat_history.append(st.session_state.messages[i])
    return chat_history

# Summarize the question along with chat history for context
def summarize_question_with_history(session, chat_history, question):
    prompt = f"""
    Based on the chat history below and the question, generate a query that extends the question 
    with the chat history provided:
    <chat_history>
    {chat_history}
    </chat_history>
    <question>
    {question}
    </question>
    """
    cmd = "SELECT snowflake.cortex.complete(?, ?) AS response"
    df_response = session.sql(cmd, params=[st.session_state.model_name, prompt]).collect()
    summary = df_response[0].RESPONSE
    if st.session_state.debug:
        st.text("Summary to be used to find similar chunks in the docs:")
        st.caption(summary)
    return summary.replace("'", "")

# Create the final prompt
def create_prompt(session, myquestion):
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history:
            question_summary = summarize_question_with_history(session, chat_history, myquestion)
            prompt_context = get_similar_chunks(session, question_summary)
        else:
            prompt_context = get_similar_chunks(session, myquestion)
    else:
        prompt_context = get_similar_chunks(session, myquestion)
        chat_history = ""

    prompt = f"""
    You are an expert chat assistance that extracts information from the CONTEXT provided
    between <context> and </context> tags. You offer a chat experience considering the information included in the CHAT HISTORY
    provided between <chat_history> and </chat_history> tags. When answering the question contained between <question> and </question> tags
    be concise and do not hallucinate. If you don’t have the information just say so. <chat_history>
    {chat_history}
    </chat_history>
    <context>
    {prompt_context}
    </context>
    <question>
    {myquestion}
    </question>
    Answer:
    """
    return prompt

# Send prompt to Snowflake Cortex for completion
def complete(session, myquestion):
    prompt = create_prompt(session, myquestion)
    cmd = "SELECT snowflake.cortex.complete(?, ?) AS response"
    df_response = session.sql(cmd, params=[st.session_state.model_name, prompt]).collect()
    return df_response

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: blue;
        color: white; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: blue;
        color: white; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)

footer="""<style>

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
<p>Developed with ❤️ by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)  
