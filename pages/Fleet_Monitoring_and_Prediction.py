import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.title(":blue[By Road Passengers predictions]")
st.write("\n")

st.write("\n")
st.write("\n")

st.write("\n")
st.write("\n")
st.write("\n")

st.write("\n")
st.title(":blue[By Air Passengers predictions]")
st.write("\n")

st.write("\n")
st.write("\n")

st.write("\n")
st.write("\n")
st.write("\n")

st.write("\n")
st.title(":blue[By Water Passengers predictions]")








years = list(range(1971, 2023))
avg_distance = [49, 49, 50, 51, 52, 51, 50, 50, 52, 57, 58, 60, 62, 67, 68, 70, 71, 71, 75, 77, 77, 78, 80, 80, 82, 85, 86, 87, 92, 94, 95, 96, 104, 106, 107, 108, 112, 118, 121, 125, 128, 127, 130, 136, 140, 141, 142, 142, 137, 130, 185, 168]
total_passengers = [2431000000, 2536000000, 2653000000, 2654000000, 2429000000, 2945000000, 3300000000, 3504000000, 3719000000, 3505000000, 3613000000, 3704000000, 3655000000, 3325000000, 3333000000, 3433000000, 3594000000, 3792000000, 3500000000, 3653000000, 3858000000, 4049000000, 3749000000, 3708000000, 3915000000, 4018000000, 4153000000, 4348000000, 4411000000, 4585000000, 4833000000, 5093000000, 4971000000, 5112000000, 5378000000, 5725000000, 6219000000, 6524000000, 6920000000, 7246000000, 7651000000, 8224000000, 8421000000, 8397000000, 8224000000, 8107000000, 8116000000, 8286000000, 8439000000, 8086000000, 1250000000, 3519000000]
non_suburban = [1204000000, 1261000000, 1268000000, 1217000000, 1056000000, 1306000000, 1498000000, 1576000000, 1606000000, 1602000000, 1613000000, 1640000000, 1626000000, 1491000000, 1449000000, 1549000000, 1577000000, 1637000000, 1495000000, 1544000000, 1599000000, 1637000000, 1467000000, 1406000000, 1485000000, 1534000000, 1575000000, 1691000000, 1743000000, 1814000000, 1972000000, 2094000000, 2037000000, 2126000000, 2200000000, 2396000000, 2705000000, 2835000000, 3118000000, 3370000000, 3590000000, 3847000000, 3944000000, 3845000000, 3719000000, 3648000000, 3550000000, 3621000000, 3655000000, 3489000000, 333000000, 1350000000]
suburban = [1227000000, 1275000000, 1385000000, 1437000000, 1373000000, 1639000000, 1802000000, 1928000000, 2113000000, 1903000000, 2000000000, 2064000000, 2029000000, 1834000000, 1884000000, 1884000000, 2017000000, 2155000000, 2005000000, 2109000000, 2259000000, 2412000000, 2282000000, 2302000000, 2430000000, 2484000000, 2578000000, 2657000000, 2668000000, 2771000000, 2861000000, 2999000000, 2934000000, 2986000000, 3178000000, 3329000000, 3514000000, 3689000000, 3802000000, 3876000000, 4061000000, 4377000000, 4477000000, 4552000000, 4505000000, 4459000000, 4566000000, 4665000000, 4784000000, 4597000000, 917000000, 2169000000]

# Create DataFrame
df = pd.DataFrame({
    'Year': years,
    'Average Distance (km)': avg_distance,
    'Total Passengers': total_passengers,
    'Non-Suburban Passengers': non_suburban,
    'Suburban Passengers': suburban
})

# Title
st.title("Indian Railways Passenger Analysis (1971-2022)")

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Average Distance Growth", 
              f"{df['Average Distance (km)'].iloc[-1] - df['Average Distance (km)'].iloc[0]} km",
              f"{((df['Average Distance (km)'].iloc[-1] - df['Average Distance (km)'].iloc[0])/df['Average Distance (km)'].iloc[0]*100):.1f}%")
with col2:
    st.metric("Peak Passenger Volume", 
              f"{df['Total Passengers'].max()/1e9:.1f}B",
              f"Year: {df.loc[df['Total Passengers'].idxmax(), 'Year']}")
with col3:
    suburban_ratio = df['Suburban Passengers'].iloc[-1] / df['Total Passengers'].iloc[-1] * 100
    st.metric("Current Suburban Ratio", 
              f"{suburban_ratio:.1f}%",
              f"vs {df['Suburban Passengers'].iloc[0] / df['Total Passengers'].iloc[0] * 100:.1f}% in 1971")

# Total Passengers Trend
st.subheader("Passenger Volume Trends")
fig1 = px.line(df, x='Year', y=['Total Passengers', 'Suburban Passengers', 'Non-Suburban Passengers'],
               title='Passenger Volume Over Time')
fig1.update_layout(yaxis_title='Number of Passengers')
st.plotly_chart(fig1, use_container_width=True)

# Average Distance Trend
st.subheader("Average Travel Distance Trend")
fig2 = px.line(df, x='Year', y='Average Distance (km)',
               title='Average Distance Travelled per Passenger')
fig2.update_layout(yaxis_title='Distance (km)')
st.plotly_chart(fig2, use_container_width=True)

# Suburban vs Non-Suburban Split
st.subheader("Suburban vs Non-Suburban Split")
fig3 = px.area(df, x='Year', y=['Suburban Passengers', 'Non-Suburban Passengers'],
               title='Passenger Distribution by Category')
fig3.update_layout(yaxis_title='Number of Passengers')
st.plotly_chart(fig3, use_container_width=True)

# Key Insights
st.subheader("Key Insights")
st.write("""
1. **Long-term Growth**: The total passenger volume showed consistent growth from 1971 to 2019, increasing from 2.4B to 8.4B passengers annually.

2. **COVID-19 Impact**: There was a significant drop in passenger numbers in 2020-2021, likely due to the COVID-19 pandemic.

3. **Average Distance Trend**: The average travel distance per passenger has increased significantly from 49km in 1971 to 168km in 2022, indicating changing travel patterns.

4. **Suburban vs Non-Suburban**: 
   - Suburban travel has generally maintained a larger share of total passengers
   - Both categories showed steady growth until 2019
   - The growth rate was higher in suburban services

5. **Recent Recovery**: Post-2020, there are signs of recovery in passenger volumes, though not yet at pre-pandemic levels.
""")

# Recommendations
st.subheader("Recommendations")
st.write("""
1. **Capacity Planning**:
   - Focus on suburban service expansion as it consistently shows higher passenger volumes
   - Plan for eventual return to pre-pandemic passenger levels

2. **Infrastructure Development**:
   - Invest in long-distance infrastructure given the trend of increasing average travel distances
   - Modernize suburban networks in major metropolitan areas

3. **Service Optimization**:
   - Balance service frequency between suburban and non-suburban routes based on passenger volume patterns
   - Consider implementing express services for longer routes

4. **Recovery Strategy**:
   - Implement measures to restore passenger confidence post-pandemic
   - Consider innovative pricing strategies to encourage ridership
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