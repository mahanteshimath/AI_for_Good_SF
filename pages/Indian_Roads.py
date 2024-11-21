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
    


st.title(":blue[🚂 🚆 Indian Road development (in KM)]")
Q1=f'''SELECT INDIAN_ROAD_CATEGORY, "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023" FROM IND_DB.IND_SCH.T01_INDIAN_ROADS'''
R1 = execute_query(Q1)
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




st.title("Vehicle Registration Analysis")


st.title(":blue[Indian Road development (in KM)]")
Q1=f'''SELECT
    replace (TITLE,  '(Month ex Telangana)','') TITLE,
    YEAR(DATE) AS YEAR,
    SUM(INDIA) AS INDIA,
    SUM(ANDHRAPRADESH) AS ANDHRAPRADESH,
    SUM(ARUNACHALPRADESH) AS ARUNACHALPRADESH,
    SUM(ASSAM) AS ASSAM,
    SUM(BIHAR) AS BIHAR,
    SUM(CHHATTISGARH) AS CHHATTISGARH,
    SUM(GOA) AS GOA,
    SUM(GUJARAT) AS GUJARAT,
    SUM(HARYANA) AS HARYANA,
    SUM(HIMACHALPRADESH) AS HIMACHALPRADESH,
    SUM(JAMMUANDKASHMIR) AS JAMMUANDKASHMIR,
    SUM(JHARKHAND) AS JHARKHAND,
    SUM(KARNATAKA) AS KARNATAKA,
    SUM(KERALA) AS KERALA,
    SUM(MADHYAPRADESH) AS MADHYAPRADESH,
    SUM(MAHARASHTRA) AS MAHARASHTRA,
    SUM(MANIPUR) AS MANIPUR,
    SUM(MEGHALAYA) AS MEGHALAYA,
    SUM(MIZORAM) AS MIZORAM,
    SUM(NAGALAND) AS NAGALAND,
    SUM(ODISHA) AS ODISHA,
    SUM(PUNJAB) AS PUNJAB,
    SUM(RAJASTHAN) AS RAJASTHAN,
    SUM(SIKKIM) AS SIKKIM,
    SUM(TAMILNADU) AS TAMILNADU,
    SUM(TRIPURA) AS TRIPURA,
    SUM(UTTARPRADESH) AS UTTARPRADESH,
    SUM(UTTARAKHAND) AS UTTARAKHAND,
    SUM(WESTBENGAL) AS WESTBENGAL,
    SUM(ANDAMANANDNICOBARISLANDS) AS ANDAMANANDNICOBARISLANDS,
    SUM(CHANDIGARH) AS CHANDIGARH,
    SUM(DELHI) AS DELHI,
    SUM(PUDUCHERRY) AS PUDUCHERRY
FROM
    IND_DB.IND_SCH.T01_IND_AUTOMOBILE_REGISTRATION
GROUP BY
    TITLE, YEAR(DATE)'''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)

df=R1_DF


# year = st.selectbox("Select Year", sorted(df["YEAR"].unique()))
# title = st.selectbox("Select Registration Type", df["TITLE"].unique())

# # Filter DataFrame based on selection
# filtered_df = df[(df["YEAR"] == year) & (df["TITLE"] == title)]
# st.write("### Filtered Data")
# st.dataframe(filtered_df)
# ''''''
# # Visualizations
# st.write("### Visualizations")

# # Line Chart of All-India Registrations Over Years
# st.write("#### All-India Registrations Over the Years")
# line_chart = px.line(df[df["TITLE"] == title], x="YEAR", y="INDIA", title=f"{title}: All-India Trend")
# st.plotly_chart(line_chart)

# # Bar Chart for Selected Year and States
# st.write("#### State-wise Registrations")
# bar_chart = px.bar(
#     filtered_df.melt(id_vars=["TITLE", "YEAR"], var_name="STATE", value_name="REGISTRATIONS"),
#     x="STATE", y="REGISTRATIONS", title=f"State-wise Registrations for {year}: {title}",
#     labels={"REGISTRATIONS": "Registrations", "STATE": "State"}
# )
# st.plotly_chart(bar_chart)




# Streamlit App
st.title("Vehicle Registration Data Viewer with Animated Visualizations")

# Display the DataFrame
st.write("### Full Dataset")
st.dataframe(df)

# Add filters
st.write("### Filter Dataset")
title = st.selectbox("Select Registration Type", df["TITLE"].unique())

# Filter DataFrame based on selection
filtered_df = df[df["TITLE"] == title]

# Visualizations
st.write("### Animated Visualizations")

# Animated Bar Chart for State-wise Registrations Over Years
st.write("#### Animated State-wise Registrations Over Years")
bar_chart = px.bar(
    filtered_df.melt(id_vars=["TITLE", "YEAR"], var_name="STATE", value_name="REGISTRATIONS"),
    x="STATE", y="REGISTRATIONS", color="STATE",
    animation_frame="YEAR", title=f"State-wise Registrations Over Years: {title}",
    labels={"REGISTRATIONS": "Registrations", "STATE": "State"},
    height=600
)
st.plotly_chart(bar_chart)

# Line Chart of All-India Registrations Over Years
st.write("#### All-India Registrations Over the Years")
line_chart = px.line(df[df["TITLE"] == title], x="YEAR", y="INDIA", title=f"{title}: All-India Trend")
st.plotly_chart(line_chart)





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