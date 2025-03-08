import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import snowflake.connector






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
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description] 
        conn.close()
        result_df = pd.DataFrame(result, columns=columns)
        return result_df
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")
        return None
    

st.title(":blue[ ✈️ Civil Aviation Analysis 1990-2019 ✈️]")

Q1=f'''SELECT * FROM  IND_DB.IND_SCH.V01_CIVIL_AVIATION_PASSENGER'''
# R1 = execute_query(Q1)
R1 = pd.read_csv('/workspaces/AI_for_Good_SF/src/V01_CIVIL_AVIATION_PASSENGER.csv')
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)
aviation_data =R1_DF

# Reshape to long format
aviation_data_long = aviation_data.melt(
    id_vars=["CIVIL_AVIATION_PASSENGER_CATEGORY"],
    var_name="Year",
    value_name="Value"
)
aviation_data_long["Year"] = pd.to_numeric(aviation_data_long["Year"])

# Sidebar for category selection
categories = aviation_data_long["CIVIL_AVIATION_PASSENGER_CATEGORY"].unique()
selected_category = st.selectbox("Select Passenger Category", categories)

# Filter data
filtered_data = aviation_data_long[
    aviation_data_long["CIVIL_AVIATION_PASSENGER_CATEGORY"] == selected_category
]

# Trend Line Chart
st.title(f"Trend Analysis for {selected_category}")
fig = px.line(filtered_data, x="Year", y="Value", title="Yearly Trend", markers=True)
st.plotly_chart(fig)

# Heatmap for all categories
st.title("Heatmap of Passenger Metrics Across Years")
pivot_data = aviation_data_long.pivot(
    index="CIVIL_AVIATION_PASSENGER_CATEGORY",
    columns="Year",
    values="Value"
)
fig_heatmap = px.imshow(pivot_data, aspect="auto", color_continuous_scale="Viridis", title="Heatmap")
st.plotly_chart(fig_heatmap)
st.markdown("""------------""")
st.header("💡 Insights and Recommendations")
st.markdown(""" 
### Analysis of Indian Civil Aviation Sector (1989-2019)

#### Key Insights

1. **Passenger Growth**
   - **Domestic**: Passenger traffic rose from 9.5 million (1989) to 140.3 million (2019), a 1,375% growth.
   - **International**: Increased from 7.7 million (1994) to 63.7 million (2019), a 727% rise.
   - **Market Share**: Private airlines dominate domestic routes, carrying 107 million passengers by 2018 compared to 16 million by public carriers.

2. **Operational Efficiency**
   - **Load Factor**: Domestic load factor rose from 69% (1993) to 86% (2019), and international from 66% (1989) to 81% (2019).
   - **Capacity**: Available seat kilometers have consistently grown, reflecting fleet expansion.

3. **Market Competition**
   - **Foreign Carriers**: In 2019, foreign airlines carried 38.1 million international passengers vs. 25.6 million by Indian airlines.
   - **Private Sector Growth**: Private airlines carried over 120 million passengers by 2018.

4. **Industry Resilience**
   - The sector demonstrated strong recovery post-2001 aviation crisis, 2008 financial crisis, and fuel price fluctuations, showing consistent growth despite disruptions.

#### Recommendations

1. **Infrastructure Development**
   - Expand airports, especially in tier-2 and tier-3 cities.
   - Invest in advanced air traffic management and ground handling systems.

2. **Market Competition**
   - Develop policies to enhance competitiveness of Indian airlines.
   - Encourage route optimization, focusing on underserved domestic and international routes.

3. **Operational Efficiency**
   - Support fleet modernization and sustainable practices.
   - Improve crew scheduling and maintenance.

4. **Regulatory Framework**
   - Streamline licensing and reduce compliance burden.
   - Encourage FDI and public-private partnerships.

5. **Customer Experience**
   - Standardize service quality and improve passenger handling.
   - Promote digital transformation with improved booking and check-in systems.

#### Future Outlook
The sector is poised for continued growth due to rising middle-class population, increasing disposable income, business travel, and tourism. By addressing infrastructure and regulatory challenges, the sector can sustain its growth trajectory and meet future demand.
 """)

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