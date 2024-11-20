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
    



Q1='''select * from IND_DB.IND_SCH.T01_INDIAN_RAILWAYS_PASSESNGER_CATEGORY'''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)



df=R1_DF
years_cols = [str(year) for year in range(1971, 2023)]
df_melted = pd.melt(df, 
                    id_vars=['CATEGORY'],
                    value_vars=years_cols,
                    var_name='Year',
                    value_name='Value')
df_melted['Year'] = pd.to_numeric(df_melted['Year'])

# Create separate dataframes for each category
avg_distance = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Average distance travelled (all passengers)']
total_passengers = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Annual)']
suburban = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Suburban) (Annual)']
non_suburban = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Non-Suburban) (Annual)']
# Title
st.title(":blue[🚂 🚆 Indian Railways Passenger Analysis (1971-2022)]")

# # Metrics
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric("Average Distance Growth", 
#               f"{df['Average Distance (km)'].iloc[-1] - df['Average Distance (km)'].iloc[0]} km",
#               f"{((df['Average Distance (km)'].iloc[-1] - df['Average Distance (km)'].iloc[0])/df['Average Distance (km)'].iloc[0]*100):.1f}%")
# with col2:
#     st.metric("Peak Passenger Volume", 
#               f"{df['Total Passengers'].max()/1e9:.1f}B",
#               f"Year: {df.loc[df['Total Passengers'].idxmax(), 'Year']}")
# with col3:
#     suburban_ratio = df['Suburban Passengers'].iloc[-1] / df['Total Passengers'].iloc[-1] * 100
#     st.metric("Current Suburban Ratio", 
#               f"{suburban_ratio:.1f}%",
#               f"vs {df['Suburban Passengers'].iloc[0] / df['Total Passengers'].iloc[0] * 100:.1f}% in 1971")

# # Total Passengers Trend
# st.subheader("Passenger Volume Trends")
# fig1 = px.line(df, x='Year', y=['Total Passengers', 'Suburban Passengers', 'Non-Suburban Passengers'],
#                title='Passenger Volume Over Time')
# fig1.update_layout(yaxis_title='Number of Passengers')
# st.plotly_chart(fig1, use_container_width=True)

# # Average Distance Trend
# st.subheader("Average Travel Distance Trend")
# fig2 = px.line(df, x='Year', y='Average Distance (km)',
#                title='Average Distance Travelled per Passenger')
# fig2.update_layout(yaxis_title='Distance (km)')
# st.plotly_chart(fig2, use_container_width=True)

# # Suburban vs Non-Suburban Split
# st.subheader("Suburban vs Non-Suburban Split")
# fig3 = px.area(df, x='Year', y=['Suburban Passengers', 'Non-Suburban Passengers'],
#                title='Passenger Distribution by Category')
# fig3.update_layout(yaxis_title='Number of Passengers')
# st.plotly_chart(fig3, use_container_width=True)

# # Key Insights
# st.subheader("Key Insights")
# st.write("""
# 1. **Long-term Growth**: The total passenger volume showed consistent growth from 1971 to 2019, increasing from 2.4B to 8.4B passengers annually.

# 2. **COVID-19 Impact**: There was a significant drop in passenger numbers in 2020-2021, likely due to the COVID-19 pandemic.

# 3. **Average Distance Trend**: The average travel distance per passenger has increased significantly from 49km in 1971 to 168km in 2022, indicating changing travel patterns.

# 4. **Suburban vs Non-Suburban**: 
#    - Suburban travel has generally maintained a larger share of total passengers
#    - Both categories showed steady growth until 2019
#    - The growth rate was higher in suburban services

# 5. **Recent Recovery**: Post-2020, there are signs of recovery in passenger volumes, though not yet at pre-pandemic levels.
# """)

# # Recommendations
# st.subheader("Recommendations")
# st.write("""
# 1. **Capacity Planning**:
#    - Focus on suburban service expansion as it consistently shows higher passenger volumes
#    - Plan for eventual return to pre-pandemic passenger levels

# 2. **Infrastructure Development**:
#    - Invest in long-distance infrastructure given the trend of increasing average travel distances
#    - Modernize suburban networks in major metropolitan areas

# 3. **Service Optimization**:
#    - Balance service frequency between suburban and non-suburban routes based on passenger volume patterns
#    - Consider implementing express services for longer routes

# 4. **Recovery Strategy**:
#    - Implement measures to restore passenger confidence post-pandemic
#    - Consider innovative pricing strategies to encourage ridership
# """)




# Melt the dataframe to convert years to rows
years_cols = [str(year) for year in range(1971, 2023)]
df_melted = pd.melt(df, 
                    id_vars=['CATEGORY'],
                    value_vars=years_cols,
                    var_name='Year',
                    value_name='Value')
df_melted['Year'] = pd.to_numeric(df_melted['Year'])

# Create separate dataframes for each category
avg_distance = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Average distance travelled (all passengers)']
total_passengers = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Annual)']
suburban = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Suburban) (Annual)']
non_suburban = df_melted[df_melted['CATEGORY'] == 'Indian Railways - Number of Passengers carried (Non-Suburban) (Annual)']

# Title and Description
st.title('Indian Railways Passenger Analysis (1971-2022)')
st.markdown("""
This dashboard analyzes Indian Railways passenger data over five decades, including total passengers,
suburban vs non-suburban travel, and average distance traveled.
""")

# Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Peak Passengers", f"{total_passengers['Value'].max()/1e9:.2f}B")
with col2:
    st.metric("Latest Avg Distance", f"{avg_distance['Value'].iloc[-1]:.0f} km")
with col3:
    growth = ((total_passengers['Value'].iloc[-2] - total_passengers['Value'].iloc[0])/total_passengers['Value'].iloc[0]) * 100
    st.metric("Passenger Growth (1971-2021)", f"{growth:.1f}%")

# Total Passengers Over Time
st.subheader('Total Passenger Traffic Trend')
fig1 = px.line(total_passengers, x='Year', y='Value',
               title='Total Passengers Over Time (1971-2022)')
fig1.update_layout(yaxis_title='Number of Passengers')
fig1.update_traces(line_color='#1f77b4')
st.plotly_chart(fig1, use_container_width=True)

# Suburban vs Non-Suburban
st.subheader('Suburban vs Non-Suburban Travel')
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=suburban['Year'], y=suburban['Value'], 
                         name='Suburban', fill='tonexty', line_color='#2ecc71'))
fig2.add_trace(go.Scatter(x=non_suburban['Year'], y=non_suburban['Value'], 
                         name='Non-Suburban', fill='tonexty', line_color='#e74c3c'))
fig2.update_layout(title='Suburban vs Non-Suburban Passenger Distribution',
                  yaxis_title='Number of Passengers')
st.plotly_chart(fig2, use_container_width=True)

# Average Distance Travelled
st.subheader('Average Distance Travelled')
fig3 = px.line(avg_distance, x='Year', y='Value',
               title='Average Distance Travelled per Passenger (km)')
fig3.update_traces(line_color='#9b59b6')
st.plotly_chart(fig3, use_container_width=True)

# Trend Analysis
st.subheader('Trend Analysis')

# Calculate compound annual growth rate (CAGR)
def calculate_cagr(start_value, end_value, num_years):
    return (((end_value / start_value) ** (1/num_years)) - 1) * 100

# Pre-pandemic analysis (2019)
total_cagr = calculate_cagr(total_passengers['Value'].iloc[0], 
                           total_passengers[total_passengers['Year']==2019]['Value'].values[0], 
                           2019-1971)

st.markdown(f"""
### Growth Metrics
- **Pre-pandemic CAGR (1971-2019)**: {total_cagr:.1f}%
- **Peak Year**: {total_passengers.loc[total_passengers['Value'].idxmax(), 'Year']}
- **Maximum Passengers**: {total_passengers['Value'].max()/1e9:.2f}B

### Key Observations
1. **Long-term Growth Trend**
   - Sustained growth from 1971 to 2019
   - Average annual growth rate of {total_cagr:.1f}%
   - Significant expansion in railway usage

2. **Travel Distance Evolution**
   - Starting average distance (1971): {avg_distance['Value'].iloc[0]:.0f} km
   - Latest average distance (2022): {avg_distance['Value'].iloc[-1]:.0f} km
   - Shows increasing preference for longer journeys

3. **Passenger Mix Trends**
   - Suburban travel consistently higher than non-suburban
   - Growing urbanization reflected in suburban numbers
   - Non-suburban travel shows steady growth
""")

# Recommendations
st.subheader('Strategic Recommendations')
st.markdown("""
1. **Infrastructure Development**
   - Invest in long-distance infrastructure to support increasing journey lengths
   - Enhance suburban network capacity in major metropolitan areas
   - Modernize existing infrastructure for better efficiency

2. **Service Optimization**
   - Increase frequency of long-distance trains
   - Optimize suburban schedules during peak hours
   - Implement dynamic pricing based on demand patterns

3. **Technology Integration**
   - Deploy smart ticketing systems
   - Implement real-time passenger information systems
   - Use data analytics for predictive maintenance

4. **Capacity Enhancement**
   - Add more coaches to existing trains
   - Introduce new routes in high-demand corridors
   - Upgrade stations to handle increased passenger flow

5. **Post-Pandemic Recovery**
   - Focus on safety measures and passenger confidence
   - Implement flexible capacity management
   - Develop contingency plans for future disruptions
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