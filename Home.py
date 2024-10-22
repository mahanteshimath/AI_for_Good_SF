import streamlit as st
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from pathlib import Path
import time
import pandas as pd
from PIL import Image
from io import BytesIO
import requests 

# --- PAGE SETUP ---
Architecture_page = st.Page(
    "pages/Architecture.py",
    title="Architecture",
    icon=":material/home:",
    default=True,
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


# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [Architecture_page],
        "Projects": [project_1_page, project_2_page],
    }
)


# --- SHARED ON ALL PAGES ---
# st.logo("src/codingisfun_logo.png")
# st.sidebar.markdown("Made with ❤️ by [Sven](https://youtube.com/@codingisfun)")




# --- RUN NAVIGATION ---
pg.run()
