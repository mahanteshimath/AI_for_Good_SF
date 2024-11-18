import streamlit as st
import snowflake.connector
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns



# Accessing the database credentials
db_credentials = st.secrets["db_credentials"]

if 'account' not in st.session_state:
    st.session_state.account = db_credentials["account"]
if 'role' not in st.session_state:
    st.session_state.role = db_credentials["role"]
if 'warehouse' not in st.session_state:
    st.session_state.warehouse = db_credentials["warehouse"]
if 'database' not in st.session_state:
    st.session_state.database = db_credentials["database"]
if 'schema' not in st.session_state:
    st.session_state.schema = db_credentials["schema"]
if 'user' not in st.session_state:
    st.session_state.user = db_credentials["user"]
if 'password' not in st.session_state:
    st.session_state.password = db_credentials["password"]
if 'weatherapi_key' not in st.session_state:
    st.session_state.weatherapi_key = db_credentials["weatherapi_key"]
    




def execute_query(query):
    try:
        conn = snowflake.connector.connect(
            account='yy95703.ap-south-1.aws',
            role=st.session_state.role,
            warehouse=st.session_state.warehouse,
            database=st.session_state.database,
            schema=st.session_state.schema,
            user=st.session_state.user,
            password=st.session_state.password,
            client_session_keep_alive=True
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description] 
        conn.close()
        result_df = pd.DataFrame(result, columns=columns) 
        return result_df
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None
    
st.title(":blue[⛽ Petrol Need Prediction ]" )
Q1='''SELECT * FROM IND_DB.IND_SCH.T01_IND_OIL_DEPENDENCY'''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)




st.markdown(
    """
    <style>
    .footer {
        background-color: #2C1E5B;  /* Match the background color */
        color: white;  /* Adjust text color for visibility */
        padding: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown('<div class="footer">Developed with ❤️ by <a href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></div>', unsafe_allow_html=True)



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
a:link , a:visited{
color: blue;
background-color: white;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: blue;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: inline; text-align: center;' href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)  