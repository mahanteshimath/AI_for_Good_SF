import streamlit as st
import streamlit.components.v1 as components



# Load the HTML content from the file
with open("./src/Architectureembed.txt", "r") as file:
    html_content = file.read()




# Display the HTML content as an embedded diagram in Streamlit
components.html(html_content, width=1200, height=800)
