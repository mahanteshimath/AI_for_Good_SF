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
    



Q1=f'''SELECT * FROM  IND_DB.IND_SCH.V01_CIVIL_AVIATION_PASSENGER'''
R1 = execute_query(Q1)
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

# Predict Future Trends Using Snowflake
st.title("Future Predictions")
st.write("Forecasting passenger trends using Snowflake ML...")


# # Forecast Query
# def get_forecast_results(category):
#     conn = get_snowflake_connection()
#     query = f"""
#         SELECT PREDICTED_VALUE, LOWER_BOUND, UPPER_BOUND, TIME 
#         FROM TABLE(SNOWFLAKE.ML.FORECAST(
#             SELECT VALUE, YEAR AS TIME 
#             FROM YOUR_TABLE 
#             WHERE CIVIL_AVIATION_PASSENGER_CATEGORY = '{category}',
#             OUTPUT_FUTURE_LENGTH => 10
#         ));
#     """
#     return pd.read_sql(query, conn)

# # Fetch predictions for the selected category
# try:
#     forecast_data = get_forecast_results(selected_category)
#     forecast_fig = px.line(
#         forecast_data,
#         x="TIME",
#         y="PREDICTED_VALUE",
#         title=f"Forecast for {selected_category}",
#         error_y="UPPER_BOUND",
#         error_y_minus="LOWER_BOUND"
#     )
#     st.plotly_chart(forecast_fig)
# except Exception as e:
#     st.error(f"Error fetching forecast data: {e}")

# # Recommendations
# st.title("Recommendations")
# if max_growth_year["Year"] > 2018:
#     st.write("**Recent Growth Spike:** Leverage marketing campaigns to maintain momentum.")
# if min_growth_year["Year"] < 2010:
#     st.write("**Historical Decline:** Investigate reasons for the decline and address operational issues.")
# st.write("**General Recommendations:** Consider using new routes or improving customer services to boost passenger numbers.")




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