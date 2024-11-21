import streamlit as st
import pandas as pd
import plotly.express as px
import snowflake.connector

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns




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
    TITLE,
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
state_filter = st.multiselect("Select State",df.columns[3:], )

vehicle_type_filter = st.multiselect("Select Vehicle Type(s)", df['TITLE'].unique())
year_filter = st.slider("Select Year Range", int(df['YEAR'].min()), int(df['YEAR'].max()), (int(df['YEAR'].min()), int(df['YEAR'].max())))

# Filter the data based on user selections
filtered_df = df
if state_filter:
    filtered_df = filtered_df[filtered_df['State'].isin(state_filter)]
if vehicle_type_filter:
    filtered_df = filtered_df[filtered_df['Vehicle Type'].isin(vehicle_type_filter)]
if year_filter:
    filtered_df = filtered_df[(filtered_df['YEAR'] >= year_filter[0]) & (filtered_df['YEAR'] <= year_filter[1])]

# Display filtered data
st.dataframe(filtered_df)

# Visualizations
st.header("Visualizations")

# Line chart for overall trend
st.subheader("Overall Registration Trend")
fig, ax = plt.subplots()
sns.lineplot(x='Month', y='Registrations', hue='Vehicle Type', data=filtered_df, ax=ax)
st.pyplot(fig)

# Bar chart for state-wise comparison
st.subheader("State-wise Registrations")
fig, ax = plt.subplots()
sns.barplot(x='State', y='Registrations', hue='Vehicle Type', data=filtered_df, ax=ax)
st.pyplot(fig)

# Heatmap for monthly registrations
st.subheader("Yearly Registrations Heatmap")
heatmap_data = filtered_df.pivot_table(values='Registrations', index='Month', columns='YEAR')
fig, ax = plt.subplots()
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='coolwarm', ax=ax)
st.pyplot(fig)



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