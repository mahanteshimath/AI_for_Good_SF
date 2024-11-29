import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


st.title(":blue[🚗 Road Accidents Analysis in India (2019-2022)]")

def create_accident_visualization():
    Q1=f'''SELECT * FROM IND_DB.IND_SCH.T01_ROAD_ACC_2019_2022'''
    R1 = execute_query(Q1)
    r1_expander = st.expander("Data sets used in this entire analysis.")
    R1_DF = pd.DataFrame(R1)
    R1_DF.index = R1_DF.index + 1
    
    data =R1_DF
    # Convert to DataFrame
    df = pd.DataFrame(data)
    # Melt the DataFrame for animation
    df_melted = df.melt(id_vars=['State'], 
                       var_name='Year', 
                       value_name='Injuries')
    r1_expander.write(R1_DF)

    # Create animated bar chart
    fig = px.bar(df_melted, 
                 x='State', 
                 y='Injuries',
                 animation_frame='Year',
                 color='Injuries',
                 range_y=[0, 25000],
                 title='Number of Persons Injured in Road Accidents by State',
                 color_continuous_scale='Reds')

    # Update layout
    fig.update_layout(
        xaxis_tickangle=-45,
        height=800,
        showlegend=False
    )

    # Display the plot
    st.plotly_chart(fig, use_container_width=True)
create_accident_visualization()


# Title and introduction
st.title(":blue[🚗 Road Accidents Analysis in India (2019-2022)]")
st.subheader(":blue[🚗This info collected from Snowflake_Powered_Accident_Analysis_bot]")
st.markdown("---")

# Create yearly comparison data
yearly_data = pd.DataFrame({
    'Year': [2019, 2022],
    'Total Accidents': [437396, 394163],
    'Fatalities': [151113, 131714],
    'Injuries': [469418, 380596],
    'NH Accidents':[146286,151997]
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


# Custom CSS styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    div[data-testid="metric-container"] {
        background-color: #F0F8FF;
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
# Key Metrics in 2022
st.subheader("Accidents Key Metrics 2022 (2019 vs 2022)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Accidents", "394,163", "12.5% ↑")
with col2:
    st.metric("Fatalities", "131,714", "16.3% ↑")
with col3:
    st.metric("Injuries", "380,596", "15.5% ↑")
with col4:
    st.metric("NH Accidents", "1,51,997", "3.9% ↑ ")

# Dashboard Layout
col1, col2 = st.columns(2)

# Yearly Comparison Chart
with col1:
    st.subheader("Yearly Comparison (2019 vs 2022)")
    fig_yearly = px.bar(yearly_data.melt(id_vars=['Year'], 
                                       value_vars=['Total Accidents', 'Fatalities', 'Injuries','NH Accidents']),
                       x='variable', y='value', color='Year', 
                       barmode='group',
                       color_discrete_sequence=['#2C3E50', '#E74C3C', '#3498DB'],
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
st.image("./src/AC5.PNG", caption="Times of India NEWS")
def add_custom_css():
    st.markdown("""
        <style>
        .flashing-title {
            font-size: 2.5em;
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
st.markdown('<div class="flashing-title">❄️RECOMMENDATIONS TO PREVENT ACCIDENTS WITH AI❄️</div>', unsafe_allow_html=True)

st.markdown("### AI-Powered Traffic Management Systems")
col1, col2 = st.columns([3, 1])

with col1:
    st.image("./src/AC1.png", caption="Traffic Management System", use_column_width=True)

with col2:
    st.markdown(
        '''
        **Implement AI-powered traffic management systems:**  
        Utilize AI to analyze real-time traffic data and optimize traffic signal timings to reduce congestion and prevent accidents.
        '''
    )

st.divider()  # Add a divider for separation

# Section 2: AI-Driven Vehicle Safety Features
st.markdown("### AI-Driven Vehicle Safety Features")
col3, col4 = st.columns([1, 3])

with col3:
    st.markdown(
        '''
        **Integrate AI-driven vehicle safety features:**  
        Equip vehicles with AI-powered safety features such as lane departure warning systems, automatic emergency braking, and collision avoidance systems.
        '''
    )

with col4:
    st.image("./src/AC2.png", caption="Vehicle Safety Features", use_column_width=True)

st.divider()  # Add a divider for separation

# Section 3: AI-Based Predictive Accident Models
st.markdown("### AI-Based Predictive Accident Models")
col4, col5 = st.columns([3, 1])

with col4:
    st.image("./src/AC3.png", caption="Predictive Accident Models", use_column_width=True)

with col5:
    st.markdown(
        '''
        **Develop AI-based predictive accident models:**  
        Use machine learning algorithms to analyze historical accident data and predict high-risk areas, enabling proactive measures to prevent accidents.
        '''
    )


st.divider()  # Add a divider for separation
col6, col7 = st.columns([1, 3])

with col6:
    st.markdown(
        '''
        **Deploy AI-powered surveillance cameras:**  
        Install AI-enabled surveillance cameras at accident-prone areas to detect and alert authorities of potential hazards in real-time.

        **Create AI-driven emergency response systems:**  
        Develop AI-powered emergency response systems that can quickly respond to accidents, providing critical care and reducing response times.

        **Implement AI-based driver behavior analysis:**  
        Use AI to analyze driver behavior and identify high-risk drivers, enabling targeted interventions to improve road safety.

        **Develop AI-powered road maintenance systems:**  
        Utilize AI to identify and prioritize road maintenance needs, ensuring that roads are safe and well-maintained.

        **Integrate AI with existing safety infrastructure:**  
        Combine AI with existing safety infrastructure, such as crash barriers and guardrails, to enhance their effectiveness.

        **Create AI-driven public awareness campaigns:**  
        Develop AI-powered public awareness campaigns to educate road users about safe driving practices and the risks of accidents.

        **Establish AI-based accident investigation systems:**  
        Use AI to analyze accident data and identify root causes, enabling more effective accident prevention strategies.
        '''
    )

with col7:
    st.image("./src/AC4.png", caption="Enhancing road safety with AI", use_column_width=True)



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
