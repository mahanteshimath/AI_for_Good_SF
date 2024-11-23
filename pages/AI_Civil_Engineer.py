import streamlit as st

st.components.v1.html(
    """
    <iframe 
        src="https://montys-multipdf-chat.streamlit.app/?embed_options=dark_theme" 
        width="100%" 
        height="800px" 
        style="border:none;">
    </iframe>
    """,
    height=800,
)
