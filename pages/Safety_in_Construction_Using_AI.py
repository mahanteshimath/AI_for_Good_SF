import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Custom CSS styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #EEE8AA;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    div[data-testid="metric-container"] > label {
        color: #1E1E1E;
        font-weight: 600;
    }
    div[data-testid="metric-container"] > div {
        color: #2C3E50;
    }
    div[data-testid="stHorizontalBlock"] {
        gap: 2rem;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🚗 Road Accidents Analysis in India (2019-2022)")
st.markdown("---")

# Create yearly comparison data
yearly_data = pd.DataFrame({
    'Year': [2019, 2022],
    'Total Accidents': [437396, 394163],
    'Fatalities': [151113, 131714],
    'Injuries': [469418, 380596]
})

# Create data for causes
causes_2019 = pd.DataFrame({
    'Cause': ['Overspeeding', 'Other Causes', 'Dangerous Driving', 'Poor Weather', 'Vehicle Defects'],
    'Percentage': [34.4, 25.6, 24.8, 8.7, 6.5]
})

# Create peak hours data
peak_hours_data = pd.DataFrame({
    'Time Period': ['6 PM - 9 PM', '3 PM - 6 PM', '9 PM - 12 AM', '12 PM - 3 PM', 'Others'],
    'Accidents': [122829, 89756, 76543, 68432, 79836]
})

# Key Metrics in 2022
st.subheader("Key Metrics (2022)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Accidents", "394,163", "12.5% ↑")
with col2:
    st.metric("Fatalities", "131,714", "16.3% ↑")
with col3:
    st.metric("Injuries", "380,596", "15.5% ↑")
with col4:
    st.metric("NH Accidents", "33.4%", "of total accidents")

# Dashboard Layout
col1, col2 = st.columns(2)

# Yearly Comparison Chart
with col1:
    st.subheader("Yearly Comparison (2019 vs 2022)")
    fig_yearly = px.bar(yearly_data.melt(id_vars=['Year'], 
                                       value_vars=['Total Accidents', 'Fatalities', 'Injuries']),
                       x='variable', y='value', color='Year', 
                       barmode='group',
                       color_discrete_sequence=['#2C3E50', '#E74C3C'],
                       title='Road Accident Statistics Comparison')
    fig_yearly.update_layout(
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2C3E50')
    )
    st.plotly_chart(fig_yearly, use_container_width=True)

# Causes Pie Chart
with col2:
    st.subheader("Major Causes of Accidents (2019)")
    fig_causes = px.pie(causes_2019, values='Percentage', names='Cause',
                       title='Distribution of Accident Causes',
                       color_discrete_sequence=px.colors.qualitative.Set3)
    fig_causes.update_layout(
        height=400,
        font=dict(color='#2C3E50')
    )
    st.plotly_chart(fig_causes, use_container_width=True)

# Peak Hours Analysis
st.subheader("Peak Hours Analysis (2019)")
fig_peak = px.bar(peak_hours_data, x='Time Period', y='Accidents',
                 title='Number of Accidents by Time Period',
                 color='Accidents',
                 color_continuous_scale='Viridis')
fig_peak.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#2C3E50')
)
st.plotly_chart(fig_peak, use_container_width=True)

# Additional Insights
st.markdown("---")
st.subheader("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Vehicle Type Impact (2022)
    - 42.5% of fatalities involved two-wheelers
    - Two-wheelers represent only 20.8% of registered vehicles
    """)

with col2:
    st.markdown("""
    ### Geographic Distribution
    - Uttar Pradesh: Highest accidents (64,211)
    - Maharashtra: Second highest (53,056)
    - Delhi: Highest among cities (19,565)
    """)


st.markdown("---")
st.subheader("Key Insights")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 2019 Key Findings
    - India ranks 1st in road accident deaths (11% of global deaths)
    - 4,49,002 total road accidents reported
    - 1,51,113 lives lost (0.20% decrease from 2018)
    - 4,51,361 persons injured (3.85% decrease)
    - 83.3% accidents occurred on national highways
    """)

with col2:
    st.markdown("""
    ### 2022 Key Findings
    - 33.4% accidents on national highways (only 1.9% of total roads)
    - Two-wheelers involved in 42.5% fatalities
    - 45.3% fatalities occurred between 6 PM and 12 AM
    - Top States: Uttar Pradesh (64,211 accidents)
    - Top City: Delhi (19,565 accidents)
    """)
# Footer
st.markdown("---")
st.markdown("Data Source: Road Accidents in India Reports (2019-2022)")