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
    



Q1=f'''select INDIAN_RAILWAYS_PASSESNGER_CATEGORY as CATEGORY, "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1984", "1985", "1986", "1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022" from IND_DB.IND_SCH.T01_INDIAN_RAILWAYS_PASSESNGER_CATEGORY'''
# R1 = execute_query(Q1)
R1 = pd.read_csv('src/T01_INDIAN_RAILWAYS_PASSESNGER_CATEGORY.csv')
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
               title='Total Passengers Over Time (1971-2022)', markers=True)
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
               title='Average Distance Travelled per Passenger (km)', markers=True)
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
st.markdown("""------------""")
st.header("💡 Insights and Recommendations")
st.markdown(""" 

- **Pre-pandemic CAGR (1971–2019):** 2.6%  
- **Peak Year:** 2019  
- **Maximum Passengers:** 8.44 billion  

#### **Key Observations**  
1. **Long-term Growth Trend**  
   - Steady growth in railway usage from 1971 to 2019 with an average annual growth rate of 2.6%.  
   - Passenger traffic has expanded significantly over the years, indicating sustained demand.  
   - Economic and population growth have been key drivers of long-term railway growth.  

2. **Travel Distance Evolution**  
   - The average travel distance increased from **49 km in 1971** to **168 km in 2022**.  
   - Longer journeys have become more common, signaling shifts in travel preferences.  
   - Increased demand for intercity and long-distance travel, reflecting socio-economic changes.  

3. **Passenger Mix Trends**  
   - Suburban travel has consistently outpaced non-suburban travel, driven by urbanization.  
   - Non-suburban travel continues to show steady growth, with increased demand for regional and intercity routes.  
   - The shift to suburban travel highlights the growing need for efficient urban transportation solutions.  

---

### Strategic Recommendations  

#### **1. Infrastructure Development**  
- **Long-Distance Infrastructure:** Build or enhance long-distance railway lines to support growing demand for longer journeys.  
- **Suburban Network Expansion:** Invest in expanding suburban networks in high-density metropolitan areas.  
- **Modernization:** Upgrade existing stations, tracks, and facilities to enhance operational efficiency.  

#### **2. Service Optimization**  
- **Train Frequency:** Increase the frequency of long-distance trains to improve accessibility and reduce congestion.  
- **Peak Hour Optimization:** Adjust suburban train schedules during peak times to better accommodate commuter traffic.  
- **Dynamic Pricing:** Introduce flexible ticket pricing based on demand patterns to optimize revenue and manage capacity.  

#### **3. Technology Integration**  
- **Smart Ticketing:** Implement digital and smart ticketing systems to streamline the booking process and reduce operational costs.  
- **Real-Time Passenger Information:** Deploy real-time tracking and communication systems for better passenger experience.  
- **Predictive Maintenance:** Use data analytics and AI to predict maintenance needs, minimizing downtime and improving reliability.  

#### **4. Capacity Enhancement**  
- **Train Expansion:** Add more coaches to existing trains to increase capacity and accommodate growing demand.  
- **New Routes:** Introduce new train routes in high-demand areas to enhance connectivity and ease congestion.  
- **Station Upgrades:** Modernize stations to handle increased passenger flow efficiently and enhance customer experience.  

#### **5. Post-Pandemic Recovery**  
- **Safety Measures:** Implement stringent safety protocols to ensure passenger confidence and maintain public health standards.  
- **Flexible Capacity Management:** Introduce flexible seating and train schedules to cater to fluctuating demand due to potential future disruptions.  
- **Contingency Planning:** Develop comprehensive contingency strategies to handle future disruptions and ensure operational continuity.  




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