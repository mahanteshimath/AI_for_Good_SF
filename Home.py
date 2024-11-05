import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path
import time
import pandas as pd
from PIL import Image
from io import BytesIO
import requests 

st.logo(
    image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
    link="https://www.linkedin.com/in/mahantesh-hiremath/",
    icon_image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
)

st.set_page_config(
  page_title="INDIAN-INFRA-AI-INSIGHTS",
  page_icon="🇮🇳",
  layout="wide",
  initial_sidebar_state="expanded",
) 

# --- PAGE SETUP ---
Architecture_page = st.Page(
    "pages/Architecture.py",
    title="Architecture",
    icon=":material/home:",
    default=True,
)
Hypothesis_page = st.Page(
    "pages/Hypothesis.py",
    title="Hypothesis",
    icon=":material/cognition:"
)
project_1_page = st.Page(
    "pages/sales_dashboard.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "pages/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)


pg = st.navigation(
    {
        "Info": [Hypothesis_page,Architecture_page],
        "SF-MP Social impact": [project_1_page, project_2_page],
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("src/codingisfun_logo.png")
# st.sidebar.markdown("Made with ❤️ by [Sven](https://youtube.com/@codingisfun)")




# --- RUN NAVIGATION ---
pg.run()
