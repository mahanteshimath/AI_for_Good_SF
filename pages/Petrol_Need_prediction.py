import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# # Configure Streamlit theme
# st.set_page_config(
#     page_title="India Oil Demand Forecast",
#     page_icon="⛽",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# Custom CSS
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #cebde0;
        --background-color: #2f1f42;
        --secondary-bg-color: #220e06;
        --text-color: #c7e5b0;
    }

    /* Global styles */
    .stApp {
        background-color: var(--background-color);
        color: var(--text-color);
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: var(--primary-color) !important;
        font-weight: bold !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }

    /* Metrics styling */
    .st-emotion-cache-1wivap2 {
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .st-emotion-cache-1wivap2:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
    }

    /* Data frame styling */
    .dataframe {
        background-color: var(--secondary-bg-color);
        border-radius: 5px;
        color: var(--text-color);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--secondary-bg-color);
        color: var(--primary-color);
        border-radius: 5px;
    }

    /* Card-like containers */
    .custom-card {
        background-color: var(--secondary-bg-color);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Plotly chart container */
    .js-plotly-plot {
        background-color: var(--secondary-bg-color);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: var(--secondary-bg-color);
        color: var(--text-color);
        text-align: center;
        padding: 1rem 0;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 999;
    }

    .footer a {
        color: var(--primary-color);
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }

    /* Button styling */
    .stButton>button {
        background-color: var(--primary-color);
        color: var(--background-color);
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }

    .stButton>button:hover {
        background-color: var(--text-color);
        transform: translateY(-2px);
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)

# Database connection function
@st.cache_resource
def init_connection():
    try:
        return snowflake.connector.connect(
            account='yy95703.ap-south-1.aws',
            role=st.session_state.role,
            warehouse=st.session_state.warehouse,
            database=st.session_state.database,
            schema=st.session_state.schema,
            user=st.session_state.user,
            password=st.session_state.password,
            client_session_keep_alive=True
        )
    except Exception as e:
        st.error(f"Failed to connect to database: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def execute_query(query):
    conn = init_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            return pd.DataFrame(result, columns=columns)
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
            return None
        finally:
            conn.close()
    return None

# App Header
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1>⛽ India's Oil Demand Forecast Dashboard</h1>
    <p style='font-size: 1.2rem; color: var(--text-color);'>
        Analyzing historical trends and predicting future oil demand till 2050
    </p>
</div>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    historical_query = '''SELECT * FROM IND_DB.IND_SCH.T01_IND_OIL_DEPENDENCY'''
    forecast_query = '''SELECT * FROM IND_DB.IND_SCH.V01_IND_OIL_DEPENDENCY_FORECAST_2050'''
    
    historical_df = execute_query(historical_query)
    forecast_df = execute_query(forecast_query)
    
    if historical_df is not None:
        historical_df['DATE'] = pd.to_datetime(historical_df['DATE'])
    if forecast_df is not None:
        forecast_df['DATE'] = pd.to_datetime(forecast_df['DATE'])
    
    return historical_df, forecast_df

historical_df, forecast_df = load_data()

if historical_df is not None and forecast_df is not None:
    # Key Metrics Section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("📊 Current Oil Metrics (2023)")
    
    latest_data = historical_df.iloc[-1]
    cols = st.columns(4)
    
    metrics_data = [
        {"label": "Domestic Production", "value": latest_data['DOMESTIC_CRUDE_OIL_PRODUCTION'], "unit": "MMT", "delta": ""},
        {"label": "Oil Imports", "value": latest_data['IMPORTS_OF_CRUDE_OIL'], "unit": "MMT", "delta": ""},
        {"label": "Total Oil Need", "value": latest_data['OIL_NEED_OF_INDIA'], "unit": "MMT", "delta": ""},
        {"label": "Import Dependency", "value": latest_data['RATIO'], "unit": "%", "delta": ""}
    ]
    
    for col, metric in zip(cols, metrics_data):
        with col:
            st.metric(
                metric["label"],
                f"{metric['value']:.1f} {metric['unit']}",
                metric["delta"]
            )
    st.markdown("</div>", unsafe_allow_html=True)

    # Forecast Visualization
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("🔮 Demand Forecast Visualization")
    
    fig = go.Figure()

    # Historical Data
    fig.add_trace(go.Scatter(
        x=forecast_df[forecast_df['ACTUAL'].notna()]['DATE'],
        y=forecast_df[forecast_df['ACTUAL'].notna()]['ACTUAL'],
        name='Historical Demand',
        line=dict(color='#cebde0', width=3)
    ))

    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast_df[forecast_df['FORECAST'].notna()]['DATE'],
        y=forecast_df[forecast_df['FORECAST'].notna()]['FORECAST'],
        name='Forecast',
        line=dict(color='#c7e5b0', width=3, dash='dash')
    ))

    # Confidence Interval
    fig.add_trace(go.Scatter(
        x=forecast_df['DATE'],
        y=forecast_df['UPPER_BOUND'],
        fill=None,
        mode='lines',
        line=dict(color='rgba(199, 229, 176, 0.1)'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=forecast_df['DATE'],
        y=forecast_df['LOWER_BOUND'],
        fill='tonexty',
        mode='lines',
        line=dict(color='rgba(199, 229, 176, 0.1)'),
        name='95% Confidence Interval',
        fillcolor='rgba(199, 229, 176, 0.1)'
    ))

    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title={
            'text': "India's Oil Demand: Historical Data and Future Projections",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(size=20, color='#cebde0')
        },
        xaxis_title="Year",
        yaxis_title="Oil Demand (MMT)",
        height=600,
        hovermode='x unified',
        legend=dict(
            bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c7e5b0')
        )
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Growth Analysis
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("📈 Growth Rate Analysis")

    first_year = forecast_df['DATE'].min().year
    current_year = 2023
    forecast_end_year = forecast_df['DATE'].max().year

    historical_start = forecast_df[forecast_df['DATE'].dt.year == first_year]['ACTUAL'].iloc[0]
    historical_end = forecast_df[forecast_df['DATE'].dt.year == current_year]['ACTUAL'].iloc[0]
    forecast_end = forecast_df[forecast_df['DATE'].dt.year == forecast_end_year]['FORECAST'].iloc[0]

    historical_years = current_year - first_year
    forecast_years = forecast_end_year - current_year

    historical_cagr = (((historical_end / historical_start) ** (1/historical_years)) - 1) * 100
    forecast_cagr = (((forecast_end / historical_end) ** (1/forecast_years)) - 1) * 100

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Historical CAGR (1999-2023)", f"{historical_cagr:.1f}%")
    with col2:
        st.metric("Projected CAGR (2024-2050)", f"{forecast_cagr:.1f}%")
    st.markdown("</div>", unsafe_allow_html=True)

    # Data Tables
    with st.expander("📋 View Historical Data"):
        st.dataframe(historical_df.style.background_gradient(cmap='YlOrRd'))
    
    with st.expander("📋 View Forecast Data"):
        st.dataframe(forecast_df.style.background_gradient(cmap='YlOrRd'))

    # Insights Section
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    st.header("💡 Key Insights")
    
    insights = [
        "**Domestic Production Trend**: Showing declining trend since 2014",
        "**Import Dependency**: Significant increase from 54.8% to 88.9%",
        "**Growth Pattern**: Moderated growth expectations in forecast period",
        "**Risk Factors**: Wider confidence intervals in long-term projections"
    ]
    
    for insight in insights:
        st.markdown(insight)
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
footer = """
<div class='footer'>
    <p>Developed with ❤️ by <a href="https://www.linkedin.com/in/mahantesh-hiremath/" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)