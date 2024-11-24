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

# --- Info ---
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

#What is wrong with Indian infra

problem = st.Page(
    "pages/Infra_Projects_Failure_Reasons.py",
    title="Infra Projects Failure Reasons",
    icon=":material/construction:",
)
AI_Civil = st.Page(
    "pages/AI_Civil_Engineer.py",
    title="AI Civil Engineer",
    icon=":material/smart_toy:",
)


#"SF-MP Social impact"
project_1_page = st.Page(
    "pages/Indian_Trains.py",
    title="Indian Trains",
    icon=":material/train:",
)

project_2_page = st.Page(
    "pages/Petrol_Need_prediction.py",
    title="Petrol Need prediction",
    icon=":material/oil_barrel:",
)

project_3_page = st.Page(
    "pages/Civil_Aviation_Analysis_Prediction.py",
    title="Civil Aviation Analysis Prediction",
    icon=":material/flight:",
)

AQI = st.Page(
    "pages/Realtime_AQI_Across_India.py",
    title="Realtime AQI Across India",
    icon=":material/aq:",
)

#"SF-MP Social impact"
project_4_page = st.Page(
    "pages/Indian_Roads.py",
    title="Indian Roads",
    icon=":material/road:",
)

 #"Open Government Data"

chatbot = st.Page(
    "pages/Snowflake_Powered_Accident_Analysis_bot.py",
    title="Snowflake Powered Accident Analysis bot",
    icon=":material/smart_toy:",
)


Accidents_Analysis_page = st.Page(
    "pages/Accidents_Analysis_Prevention_Using_AI.py",
    title="Accidents Analysis Prevention Using AI",
    icon=":material/car_crash:",
)
Severity_Prediction = st.Page(
    "pages/Accident_Severity_Prediction_Using_AI.py",
    title="Accident Severity Prediction_Using AI",
    icon=":material/car_crash:",
)




pg = st.navigation(
    {
        "Info": [Hypothesis_page,Architecture_page],
        "What is wrong with Indian infra": [problem,AI_Civil],
        "SF-MP Social impact Data": [project_4_page,project_1_page,project_3_page,project_2_page,AQI],
        "Open Government Data":[chatbot,Accidents_Analysis_page,Severity_Prediction],
    }
)


pg.run()
