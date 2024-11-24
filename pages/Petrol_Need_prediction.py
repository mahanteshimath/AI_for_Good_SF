import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Function to execute Snowflake query
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

# Set up the page title
st.title(":blue[⛽ Petrol Need Prediction Till 2050]")

# Query the data
Q1 = '''SELECT * FROM IND_DB.IND_SCH.T01_IND_OIL_DEPENDENCY'''
R1 = execute_query(Q1)

if R1 is not None:
    # Clean and prepare data
    df = pd.DataFrame(R1)
    df.columns = map(str.upper, df.columns)
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')

    # Fix for NaN or invalid numeric values
    numeric_cols = ['DOMESTIC_CRUDE_OIL_PRODUCTION', 'IMPORTS_OF_CRUDE_OIL', 'OIL_NEED_OF_INDIA', 'RATIO']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Display dataset in an expander
    r1_expander = st.expander("Data sets used in this entire analysis.")
    df.index = df.index + 1
    r1_expander.write(df)

    # Key Metrics
    st.header("Key Metrics (2023)")
    col1, col2, col3, col4 = st.columns(4)
    latest_row = df.iloc[-1]
    with col1:
        st.metric("Domestic Production", f"{latest_row['DOMESTIC_CRUDE_OIL_PRODUCTION']:.2f} MMT")
    with col2:
        st.metric("Oil Imports", f"{latest_row['IMPORTS_OF_CRUDE_OIL']:.2f} MMT")
    with col3:
        st.metric("Total Oil Need", f"{latest_row['OIL_NEED_OF_INDIA']:.2f} MMT")
    with col4:
        st.metric("Import Dependency", f"{latest_row['RATIO']:.1f}%")

    # Time Series Plot
    st.header("Oil Production and Imports Over Time")
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(x=df['DATE'], y=df['DOMESTIC_CRUDE_OIL_PRODUCTION'],
                   name="Domestic Production", line=dict(color='green')),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df['DATE'], y=df['IMPORTS_OF_CRUDE_OIL'],
                   name="Imports", line=dict(color='red')),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df['DATE'], y=df['RATIO'],
                   name="Import Dependency Ratio", line=dict(color='orange', dash='dot')),
        secondary_y=True
    )

    fig.update_layout(
        title="Oil Production, Imports, and Import Dependency Ratio",
        xaxis_title="Year",
        yaxis_title="Million Metric Tonnes (MMT)",
        yaxis2_title="Import Dependency Ratio (%)",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    # Query Forecast Data
    Q2 = '''SELECT * FROM IND_DB.IND_SCH.V01_IND_OIL_DEPENDENCY_FORECAST_2050'''
    R2 = execute_query(Q2)

    if R2 is not None:
        # Clean and prepare forecast data
        forecast_df = pd.DataFrame(R2)
        forecast_df.columns = map(str.upper, forecast_df.columns)
        forecast_df['DATE'] = pd.to_datetime(forecast_df['DATE'], errors='coerce')

        # Fix for NaN or invalid numeric values in forecast data
        numeric_cols_forecast = ['ACTUAL', 'FORECAST', 'UPPER_BOUND', 'LOWER_BOUND']
        for col in numeric_cols_forecast:
            forecast_df[col] = pd.to_numeric(forecast_df[col], errors='coerce')

        # Display forecast dataset in an expander
        r2_expander = st.expander("Forecast Data Used in Analysis")
        forecast_df.index = forecast_df.index + 1
        r2_expander.write(forecast_df)

        # Key Metrics for Forecast
        st.header("Key Metrics")
        col1, col2, col3, col4 = st.columns(4)
        current_demand=262
        with col1:
            current_demand = forecast_df['ACTUAL'].iloc[-1]
            st.metric("Current Demand (2023)", f"{current_demand:.0f} MMT",
                      f"{current_demand - forecast_df['ACTUAL'].iloc[-2]:.1f} MMT")

        with col2:
            forecast_2030 = forecast_df[forecast_df['DATE'].dt.year == 2030]['FORECAST'].values[0]
            st.metric("Projected Demand (2030)", f"{forecast_2030:.0f} MMT",
                      f"{forecast_2030 - current_demand:.1f} MMT")

        with col3:
            forecast_2040 = forecast_df[forecast_df['DATE'].dt.year == 2040]['FORECAST'].values[0]
            st.metric("Projected Demand (2040)", f"{forecast_2040:.0f} MMT",
                      f"{forecast_2040 - forecast_2030:.1f} MMT")

        with col4:
            forecast_2050 = forecast_df[forecast_df['DATE'].dt.year == 2050]['FORECAST'].values[0]
            st.metric("Projected Demand (2050)", f"{forecast_2050:.0f} MMT",
                      f"{forecast_2050 - forecast_2040:.1f} MMT")

        # Main Plot for Forecast Data
        st.header("Historical Data and Forecast Visualization")

        fig = go.Figure()

        # Historical Data
        fig.add_trace(go.Scatter(
            x=forecast_df['DATE'][forecast_df['ACTUAL'].notna()],
            y=forecast_df['ACTUAL'][forecast_df['ACTUAL'].notna()],
            name='Historical Demand',
            line=dict(color='blue', width=2)
        ))

        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['DATE'][forecast_df['FORECAST'].notna()],
            y=forecast_df['FORECAST'][forecast_df['FORECAST'].notna()],
            name='Forecast',
            line=dict(color='red', width=2, dash='dash')
        ))

        # Confidence Interval
        fig.add_trace(go.Scatter(
            x=forecast_df['DATE'],
            y=forecast_df['UPPER_BOUND'],
            fill=None,
            mode='lines',
            line_color='rgba(255,0,0,0)',
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=forecast_df['DATE'],
            y=forecast_df['LOWER_BOUND'],
            fill='tonexty',
            mode='lines',
            line_color='rgba(255,0,0,0)',
            name='95% Confidence Interval',
            fillcolor='rgba(255,0,0,0.1)'
        ))

        fig.update_layout(
            title="India's Oil Demand: Historical Data and Future Projections",
            xaxis_title="Year",
            yaxis_title="Oil Demand (MMT)",
            height=600,
            hovermode='x unified'
        )

        st.plotly_chart(fig, use_container_width=True)

# Footer Section
footer = """
<style>
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
<p>Developed with ❤️ by <a style='display: inline;' href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
