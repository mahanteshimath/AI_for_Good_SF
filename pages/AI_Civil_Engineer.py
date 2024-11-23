import streamlit as st

st.components.v1.html(
    """
    <iframe 
        src="https://montys-multipdf-chat.streamlit.app/?embed=true" 
        style="height: 100%; width: 100%; border: none;">
    </iframe>
    """,
    height=800,
)
