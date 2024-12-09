import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas


st.logo(
    image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
    link="https://www.linkedin.com/in/mahantesh-hiremath/",
    icon_image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
)


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
if 'google_api_key' not in st.session_state:
    st.session_state.google_api_key = db_credentials["google_api_key"]
    

def store_credentials():
    st.session_state.account = db_credentials["account"]
    st.session_state.role = db_credentials["role"]
    st.session_state.warehouse = db_credentials["warehouse"]
    st.session_state.database = db_credentials["database"]
    st.session_state.schema = db_credentials["schema"]
    st.session_state.user = db_credentials["user"]
    st.session_state.password = db_credentials["password"]

def create_snowflake_connection():
    try:
        conn = snowflake.connector.connect(
            account=st.session_state.account,
            role=st.session_state.role,
            warehouse=st.session_state.warehouse,
            database=st.session_state.database,
            schema=st.session_state.schema,
            user=st.session_state.user,
            password=st.session_state.password,
            client_session_keep_alive=True
        )
        st.toast("Connection to Snowflake successfully!", icon='🎉')
        time.sleep(.5)
        st.balloons()
    except Exception as e:
        st.error(f"Error connecting to Snowflake: {str(e)}")
    return conn

def execute_query(query):
    try:
        conn = snowflake.connector.connect(
            account=st.session_state.account,
            role=st.session_state.role,
            warehouse=st.session_state.warehouse,
            database=st.session_state.database,
            schema=st.session_state.schema,
            user=st.session_state.user,
            password=st.session_state.password,
            client_session_keep_alive=True
        )
        cursor = conn.cursor()
        cursor.execute(f"USE DATABASE {st.session_state.database}")
        cursor.execute(f"USE SCHEMA {st.session_state.schema}")
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        conn.close()
        result_df = pd.DataFrame(result, columns=columns)
        return result_df
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None








def add_custom_css():
    st.markdown("""
        <style>
        .flashing-title {
            font-size: 1.7em;
            font-weight: bold;
            color: #4CAF50;
            animation: flash 2s infinite;
        }
        @keyframes flash {
            0% { opacity: 1; }
            30% { opacity: 0; }
            100% { opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

add_custom_css()
st.markdown('<div class="flashing-title">❄️INDIAN-INFRA-AI-INSIGHTS❄️</div>', unsafe_allow_html=True)


col1, col2 = st.columns(2, gap="small")
with col1:
    st.image("./src/India.jpeg")

with col2:
    st.title("Hypothesis", anchor=False)
    st.write(
        '''Giving more focus on infra development lead to overall country development in all angles best examples are Dubai and Singapore. We can learn from proven strategies and implementing them with productively will help to India to become developed country.
   Leveraging AI-driven analytics for urban infrastructure such as predictive maintenance, public transport optimization, energy forecasting, smart waste management, disaster resilience, and affordable housing can greatly enhance sustainability and quality of life in Indian megacities.'''
    )
    st.write("\n")
    st.write(
        '''Finally my point is sometimes building one bridge helped villages to improve economically i.e people can transport goods or youth can go for jobs or higher education.'''
    )
st.markdown("""---------------------------------""")
st.write("\n")

st.write("\n")
st.title("Girish Bharadwaj: Bridge Man of India")


article_content = """
### Girish Bharadwaj: How a Hole in a Boat Led to the Emergence of Bridge Man of India
*(Excerpt from The New Indian Express)*

Girish Bharadwaj, known as the "Bridge Man of India," has transformed rural connectivity in India by building over 130 bridges across various states, including Karnataka, Kerala, Telangana, and Odisha. His journey began in 1989 when residents of Aramburu village, tired of relying on a boat that frequently broke down, approached him to construct a footbridge. Despite being a mechanical engineer with no prior experience in bridge construction, Bharadwaj was inspired by the villagers' determination and decided to help.

He designed a low-cost hanging bridge with assistance from engineering friends and local villagers, completing the project for under ₹2 lakh. This initial success led to government collaboration, expanding his efforts to connect isolated communities. Bharadwaj's bridges are notable for their cost-effectiveness and durability, often surpassing their intended lifespan of 10-20 years.

His innovative approach draws inspiration from famous suspension bridges like San Francisco's Golden Gate Bridge while adapting designs to local needs. He has received recognition for his contributions, including the Padma Shri award in 2017. Now, his son continues his legacy as demand shifts towards larger structures due to increased vehicle use. Bharadwaj’s work not only improved infrastructure but also empowered rural communities by connecting them to broader opportunities.

...

For more details, please refer to the [full article on The New Indian Express](https://www.newindianexpress.com/good-news/2020/Nov/15/girish-bharadwajhow-a-hole-in-a-boat-led-to-the-emergence-of-bridge-man-of-india-2223737.html).
"""

st.markdown(article_content)

st.markdown("""---------------------------------""")

# Creating the budget allocation data as a DataFrame
st.title("Budget Allocation in infrastructure(in lakh crore) by Financial Year")
Q1='''SELECT * FROM IND_DB.IND_SCH.T01_INFRASTRUCTURE_BUDGET'''
R1 = execute_query(Q1)
r1_expander = st.expander("Budget Allocation Data")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)
df = R1_DF

plt.figure(figsize=(8, 6))
bars = plt.bar(df["FINANCIAL_YEAR"], df["BUDGET_ALLOCATION"], color='skyblue')
plt.title("Budget Allocation in infrastructure(in lakh crore) by Financial Year")
plt.xlabel("FINANCIAL_YEAR")
plt.ylabel("BUDGET_ALLOCATION")
plt.xticks(rotation=45)
plt.grid(axis='y')

# Add values on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

# Display the chart in Streamlit
st.pyplot(plt)








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
