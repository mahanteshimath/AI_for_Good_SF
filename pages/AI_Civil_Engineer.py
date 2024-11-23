import streamlit as st
st.title("🤖 AI assistant specialized in Civil 🌉 Engineering")
st.components.v1.html(
    """
    <iframe 
        src="https://montys-multipdf-chat.streamlit.app//?embed=true&embed_options=hide_loading_screen" 
        style="height: 800px; width: 100%; border: none;">
    </iframe>
    """,
    height=800,
)

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
