import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime


# Add custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Create sample data
@st.cache_data
def load_data():
    # Yearly statistics
    yearly_stats = pd.DataFrame({
        'Year': [2019, 2020, 2021, 2022],
        'Total Accidents': [437396, 366138, 350354, 394163],
        'Fatalities': [151113, 131714, 133899, 168491],
        'Injuries': [469418, 348279, 355796, 380596]
    })
    
    # State-wise data (sample data)
    states = ['Uttar Pradesh', 'Maharashtra', 'Tamil Nadu', 'Karnataka', 'Madhya Pradesh', 
              'Kerala', 'Gujarat', 'Rajasthan', 'Bihar', 'Andhra Pradesh']
    state_data = pd.DataFrame({
        'State': states,
        'Accidents_2022': [64211, 53056, 47122, 41405, 39763, 33469, 31725, 28985, 27252, 26246],
        'Fatalities_2022': [21792, 16255, 16685, 11141, 14075, 3481, 8974, 10850, 9786, 8632],
        'Injuries_2022': [45123, 39875, 42356, 35687, 32456, 29876, 27654, 25432, 23456, 21345]
    })
    
    return yearly_stats, state_data

yearly_stats, state_data = load_data()

# Sidebar for global filters
st.sidebar.header("📊 Dashboard Controls")

# Year range selector
selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=2019,
    max_value=2022,
    value=(2019, 2022)
)

# Metric selector
selected_metrics = st.sidebar.multiselect(
    "Select Metrics to Display",
    ["Total Accidents", "Fatalities", "Injuries"],
    default=["Total Accidents", "Fatalities", "Injuries"]
)

# Main dashboard
st.title("🚗 Road Accidents in India Interactive Dashboard")
st.markdown(f"### Analysis Period: {selected_years[0]} - {selected_years[1]}")

# Top metrics with animation
col1, col2, col3 = st.columns(3)
latest_year = 2022
prev_year = 2021

with col1:
    current = yearly_stats[yearly_stats['Year'] == latest_year]['Total Accidents'].values[0]
    previous = yearly_stats[yearly_stats['Year'] == prev_year]['Total Accidents'].values[0]
    pct_change = ((current - previous) / previous * 100)
    st.metric("Total Accidents", f"{current:,}", f"{pct_change:.1f}% vs {prev_year}")

with col2:
    current = yearly_stats[yearly_stats['Year'] == latest_year]['Fatalities'].values[0]
    previous = yearly_stats[yearly_stats['Year'] == prev_year]['Fatalities'].values[0]
    pct_change = ((current - previous) / previous * 100)
    st.metric("Fatalities", f"{current:,}", f"{pct_change:.1f}% vs {prev_year}")

with col3:
    current = yearly_stats[yearly_stats['Year'] == latest_year]['Injuries'].values[0]
    previous = yearly_stats[yearly_stats['Year'] == prev_year]['Injuries'].values[0]
    pct_change = ((current - previous) / previous * 100)
    st.metric("Injuries", f"{current:,}", f"{pct_change:.1f}% vs {prev_year}")

# Interactive Trends Analysis
st.header("📈 Trend Analysis")
trend_tab1, trend_tab2 = st.tabs(["Yearly Trends", "State-wise Analysis"])

with trend_tab1:
    # Filter data based on selected years and metrics
    filtered_data = yearly_stats[
        (yearly_stats['Year'] >= selected_years[0]) & 
        (yearly_stats['Year'] <= selected_years[1])
    ]
    
    melted_data = filtered_data.melt(
        id_vars=['Year'],
        value_vars=selected_metrics,
        var_name='Metric',
        value_name='Count'
    )
    
    fig = px.line(melted_data,
                  x='Year',
                  y='Count',
                  color='Metric',
                  title='Yearly Trends',
                  markers=True)
    
    fig.update_layout(
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with trend_tab2:
    # State selector
    selected_state = st.selectbox("Select State", state_data['State'].unique())
    
    # Filter state data
    state_metrics = state_data[state_data['State'] == selected_state].melt(
        id_vars=['State'],
        value_vars=['Accidents_2022', 'Fatalities_2022', 'Injuries_2022'],
        var_name='Metric',
        value_name='Count'
    )
    
    fig = px.bar(state_metrics,
                 x='Metric',
                 y='Count',
                 title=f'Statistics for {selected_state} (2022)',
                 color='Metric')
    
    st.plotly_chart(fig, use_container_width=True)

# Time Analysis Section
st.header("⏰ Temporal Analysis")
time_tab1, time_tab2 = st.tabs(["Daily Distribution", "Monthly Trends"])

with time_tab1:
    time_data = pd.DataFrame({
        'Time_Period': ['12 AM - 6 AM', '6 AM - 12 PM', '12 PM - 6 PM', '6 PM - 12 AM'],
        'Percentage': [15.2, 25.1, 24.4, 35.3]
    })
    
    # Add interactive time selection
    selected_period = st.select_slider(
        "Select Time Period",
        options=time_data['Time_Period'].tolist(),
        value=time_data['Time_Period'].tolist()[0]
    )
    
    fig = go.Figure(data=[
        go.Bar(x=time_data['Time_Period'],
               y=time_data['Percentage'],
               marker_color=['royalblue' if x == selected_period else 'lightgray' 
                           for x in time_data['Time_Period']])
    ])
    
    fig.update_layout(
        title='Distribution of Accidents by Time of Day',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

with time_tab2:
    monthly_data = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        'Accidents': [8.5, 7.8, 8.2, 8.0, 8.4, 8.1, 8.3, 8.6, 8.4, 8.5, 8.3, 8.9]
    })
    
    fig = px.line(monthly_data,
                  x='Month',
                  y='Accidents',
                  title='Monthly Distribution of Accidents (%)',
                  markers=True)
    
    st.plotly_chart(fig, use_container_width=True)

# Interactive Risk Analysis
st.header("🎯 Risk Analysis")
risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    # Vehicle Type Analysis
    vehicle_data = pd.DataFrame({
        'Vehicle_Type': ['Two-wheelers', 'Cars', 'Trucks', 'Buses', 'Others'],
        'Percentage': [42.5, 23.6, 19.1, 8.9, 5.9]
    })
    
    # Interactive vehicle selection
    selected_vehicle = st.radio("Select Vehicle Type", vehicle_data['Vehicle_Type'].tolist())
    
    fig = px.pie(vehicle_data,
                 values='Percentage',
                 names='Vehicle_Type',
                 title='Distribution by Vehicle Type')
    
    fig.update_traces(
        marker=dict(colors=['royalblue' if x == selected_vehicle else 'lightgray' 
                           for x in vehicle_data['Vehicle_Type']])
    )
    
    st.plotly_chart(fig, use_container_width=True)

with risk_col2:
    # Road Type Analysis
    road_data = pd.DataFrame({
        'Road_Type': ['National Highway', 'State Highway', 'Urban Roads', 'Rural Roads'],
        'Percentage': [33.4, 25.6, 24.8, 16.2]
    })
    
    fig = px.bar(road_data,
                 x='Road_Type',
                 y='Percentage',
                 title='Accidents by Road Type (%)')
    
    st.plotly_chart(fig, use_container_width=True)

# Interactive Insights
st.header("💡 Dynamic Insights")
insight_type = st.selectbox(
    "Select Analysis Type",
    ["Temporal Patterns", "Vehicle Analysis", "Geographic Distribution"]
)

insights = {
    "Temporal Patterns": """
    - Peak accident hours are between 6 PM and 12 AM (35.3% of accidents)
    - Weekend accidents are 15% higher than weekdays
    - Holiday seasons show 20% increase in accident rates
    """,
    "Vehicle Analysis": """
    - Two-wheelers account for 42.5% of all fatalities
    - Commercial vehicles involved in 28% of total accidents
    - Single-vehicle accidents constitute 34.1% of total incidents
    """,
    "Geographic Distribution": """
    - Urban areas account for 56.3% of total accidents
    - National highways see 33.4% of accidents despite being 1.9% of road network
    - Top 10 states account for 75.4% of total accidents
    """
}

st.markdown(insights[insight_type])

# Export Options
st.header("📤 Export Dashboard")
col1, col2 = st.columns(2)

with col1:
    if st.button("Export as PDF"):
        st.info("Generating PDF report... (This is a demo button)")

with col2:
    if st.button("Export as Excel"):
        st.info("Generating Excel report... (This is a demo button)")

# Footer with last update time
st.markdown("---")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")