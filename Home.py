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

#"SF-MP Social impact"
project_1_page = st.Page(
    "pages/Fleet_Monitoring_and_Prediction.py",
    title="Fleet Monitoring and Prediction.py",
    icon=":material/road:",
)


 #"Open Government Data"
road_page = st.Page(
    "pages/Road_Accidents_Prevention_Using_AI.py",
    title="Road Accidents Prevention Using_AI",
    icon=":material/bar_chart:",
)

safety_page = st.Page(
    "pages/Safety_in_Construction_Using_AI.py",
    title="Safety in Construction Using AI",
    icon=":material/health_and_safety:",
)

chatbot = st.Page(
    "pages/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)
pg = st.navigation(
    {
        "Info": [Hypothesis_page,Architecture_page],
        "SF-MP Social impact": [project_1_page],
        "Open Government Data":[road_page, safety_page,chatbot],
    }
)


pg.run()
