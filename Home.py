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
Hypothesis_page = st.Page(
    "pages/Hypothesis.py",
    title="Hypothesis",
    icon=":material/cognition:",
    default=True,
)
Architecture_page = st.Page(
    "pages/Architecture.py",
    title="Architecture",
    icon=":material/home:"

)


#"SF-MP Social impact"
project_1_page = st.Page(
    "pages/Fleet_Monitoring_and_Prediction.py",
    title="Fleet Monitoring and Prediction",
    icon=":material/road:",
)

project_2_page = st.Page(
    "pages/Petrol_Need_prediction.py",
    title="Petrol Need prediction",
    icon=":material/oil_barrel:",
)


 #"Open Government Data"
road_page = st.Page(
    "pages/Accidents_Prevention_Using_AI.py",
    title="Accidents Prevention Using AI",
    icon=":material/car_crash:",
)

safety_page = st.Page(
    "pages/Safety_in_Construction_Using_AI.py",
    title="Safety in Construction Using AI",
    icon=":material/health_and_safety:",
)
Drowsiness = st.Page(
    "pages/Drowsiness_Detection.py",
    title="Drowsiness Detection",
    icon=":material/swap_driving_apps_wheel:",
)
PMAY = st.Page(
    "pages/PMAY_AI.py",
    title="PMAY Analysis Using AI",
    icon=":material/house:",
)
chatbot = st.Page(
    "pages/Snowflake_chatbot.py",
    title="Snowflake chatbot",
    icon=":material/smart_toy:",
)

pg = st.navigation(
    {
        "Info": [Hypothesis_page,Architecture_page],
        "SF-MP Social impact Data": [project_1_page,project_2_page],
        "Open Government Data":[road_page, safety_page,Drowsiness,PMAY,chatbot],
    }
)


pg.run()
