# import streamlit as st

# st.components.v1.html(
#     """
#     <iframe 
#         src="https://montys-multipdf-chat.streamlit.app//?embed=true&embed_options=show_colored_line&embed_options=disable_scrolling" 
#         style="height: 800px; width: 100%; border: none;">
#     </iframe>
#     """,
#     height=800,
# )


import streamlit as st

# Embed the external app and make the iframe fit the page
st.components.v1.html(
    """
    <style>
        .iframe-container {
            position: relative;
            width: 100%;
            height: 100vh; /* Full viewport height */
            overflow: hidden;
        }
        .iframe-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
    <div class="iframe-container">
        <iframe 
            src="https://montys-multipdf-chat.streamlit.app//?embed=true&embed_options=show_colored_line">
        </iframe>
    </div>
    """,
    height=0,  # Let the CSS handle the height
)
