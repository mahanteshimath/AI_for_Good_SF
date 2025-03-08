import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objects as go



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
    


st.title(":blue[ 🛣️ Indian Roads development (in KM) 2001-2023]")
Q1=f'''SELECT INDIAN_ROAD_CATEGORY, "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023" FROM IND_DB.IND_SCH.T01_INDIAN_ROADS'''
R1 = execute_query(Q1)
# R1 = execute_query(Q1)
R1 = pd.read_csv('src/T01_IND_OIL_DEPENDENCY.csv')
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)



road_data=R1_DF

road_data_long = road_data.melt(
    id_vars=["INDIAN_ROAD_CATEGORY"],
    var_name="Year",
    value_name="Value"
)
road_data_long["Year"] = pd.to_numeric(road_data_long["Year"])

# Sidebar for category selection
categories = road_data_long["INDIAN_ROAD_CATEGORY"].unique()
selected_category = st.selectbox("Select Passenger Category", categories)

# Filter data
filtered_data = road_data_long[
    road_data_long["INDIAN_ROAD_CATEGORY"] == selected_category
]

# Trend Line Chart
st.title(f"Trend Analysis for {selected_category} (in KM)")
fig = px.line(filtered_data, x="Year", y="Value", title="Yearly Trend", markers=True)
st.plotly_chart(fig)


st.markdown("""------------""")

st.title(":blue[Vehicle Registration Analysis 2018-2021]")
Q1=f'''SELECT *
FROM
    IND_DB.IND_SCH.V01_IND_AUTOMOBILE_REGISTRATION_DATA
     '''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)

df=R1_DF

# Add filters
st.write("### Filter Dataset")
title = st.selectbox("Select Registration Type", df["TITLE"].unique())

# Filter DataFrame based on selection
filtered_df = df[df["TITLE"] == title]
st.write("#### Animated State-wise Registrations Over Years")
bar_chart = px.bar(
    filtered_df.melt(id_vars=["TITLE", "YEAR"], var_name="STATE", value_name="REGISTRATIONS"),
    x="STATE", y="REGISTRATIONS", color="STATE",
    animation_frame="YEAR", title=f"State-wise Registrations Over Years: {title}",
    labels={"REGISTRATIONS": "Registrations", "STATE": "State"},
    height=600
)
st.plotly_chart(bar_chart)
st.write("#### All-India Registrations Over the Years")
Q2=f'''SELECT TITLE,YEAR,INDIA FROM     IND_DB.IND_SCH.V01_IND_AUTOMOBILE_REGISTRATION_DATA
     WHERE TITLE='{title}'
     '''
R2 = execute_query(Q2)
r2_expander = st.expander("Data sets used in this entire analysis.")
R2_DF = pd.DataFrame(R2)
R2_DF.index = R2_DF.index + 1
r2_expander.write(R2_DF)


# Line Chart of All-India Registrations Over Years

line_chart = px.line(R2_DF, x="YEAR", y="INDIA", title=f"{title}: All-India Trend", markers=True)
st.plotly_chart(line_chart)
st.markdown("""------------""")
st.header("💡 Insights and Recommendations")
st.markdown("""  

### Insights and Recommendations for Vehicle Registration Analysis (2018–2021)

1. **Overall National Trend**:
   - Vehicle registrations peaked in 2018 (47.33 million) and steadily declined in subsequent years.
   - The sharpest drop occurred in 2020 (35.02 million), likely due to the COVID-19 pandemic, with a slight recovery in 2021 (35.41 million).

2. **State-Wise Trends**:
   - **Consistently High Registrations**:
     - States like **Uttar Pradesh**, **Maharashtra**, and **Tamil Nadu** had the highest registrations across all years, contributing significantly to national totals.
   - **Significant Declines**:
     - States like **Delhi** and **Kerala** showed notable decreases in registrations post-2018, reflecting potential market saturation or economic impacts.
   - **Smaller States**:
     - States like **Sikkim**, **Goa**, and **Arunachal Pradesh** contributed marginally to the totals but showed consistent patterns year-on-year.

3. **Impact of the Pandemic (2020)**:
   - Vehicle registrations declined across all states, with smaller states seeing the steepest relative drops.
   - Economic uncertainties and mobility restrictions were likely drivers of this decline.


---

#### Recommendations
1. **Policy Interventions for Recovery**:
   - **Tax Incentives**: Introduce temporary tax benefits for vehicle purchases to stimulate demand, especially in states with significant drops.
   - **Support for EV Adoption**: Leverage the recovery to promote electric vehicle registrations, focusing on states like Delhi, which already show EV momentum.

2. **Targeted State Policies**:
   - **Underperforming States**: Focus on states like **Bihar**, **Jharkhand**, and **Odisha** to explore barriers to vehicle adoption and offer localized incentives.
   - **Small States**: Encourage vehicle leasing models in smaller states like **Goa** and **Sikkim** to address affordability concerns.

3. **Post-Pandemic Adjustments**:
   - Collaborate with vehicle manufacturers to boost financing options for consumers impacted during the pandemic.
   - Introduce rural-focused vehicle financing schemes to enhance registrations in states like **Uttar Pradesh** and **Bihar**.


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