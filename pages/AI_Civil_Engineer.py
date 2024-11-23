import streamlit as st

st.components.v1.html(
    """
    <iframe 
        src="https://montys-multipdf-chat.streamlit.app//?embed=true&embed_options=show_colored_line" 
        style="height: 800px; width: 100%; border: none;">
    </iframe>
    """,
    height=800,
)

