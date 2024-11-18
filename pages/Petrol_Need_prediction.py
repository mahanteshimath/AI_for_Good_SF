import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np



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
    
st.title(":blue[⛽ Petrol Need Prediction Till 2050 ]" )
Q1='''SELECT * FROM IND_DB.IND_SCH.T01_IND_OIL_DEPENDENCY'''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)


df=R1_DF
# Key Metrics
st.header("Key Metrics (2023)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Domestic Production", f"{df['DOMESTIC_CRUDE_OIL_PRODUCTION'].iloc[-1]} MMT")
with col2:
    st.metric("Oil Imports", f"{df['IMPORTS_OF_CRUDE_OIL'].iloc[-1]} MMT")
with col3:
    st.metric("Total Oil Need", f"{df['OIL_NEED_OF_INDIA'].iloc[-1]} MMT")
with col4:
    st.metric("Import Dependency", f"{df['RATIO'].iloc[-1]:.1f}%")

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

# Analysis and Insights
st.header("📊 Key Insights")

st.markdown("""
1. **Increasing Import Dependency**
   - Import dependency has risen from 54.8% in 1999 to 88.9% in 2023
   - Domestic production has declined from 33 MMT to 29 MMT in the same period
   
2. **Production Trends**
   - Domestic production peaked at 38 MMT during 2011-2014
   - There's been a consistent decline in domestic production since 2014
   
3. **Import Growth**
   - Imports have increased significantly from 40 MMT in 1999 to 233 MMT in 2023
   - Brief decline in imports during 2020-21 (COVID-19 impact)
   
4. **Total Consumption**
   - Overall oil need has grown from 73 MMT to 262 MMT (259% increase)
   - Average annual growth rate of 5.4% in total consumption
""")

# Recommendations
st.header("💡 Recommendations")

st.markdown("""
1. **Diversify Energy Sources**
   - Invest in renewable energy infrastructure
   - Promote electric vehicles and public transportation
   - Develop alternative fuel sources like biofuels

2. **Boost Domestic Production**
   - Invest in exploration of new oil fields
   - Implement enhanced oil recovery techniques
   - Modernize existing production infrastructure

3. **Strategic Reserves**
   - Expand strategic petroleum reserves
   - Develop better storage infrastructure
   - Implement smart inventory management

4. **Policy Measures**
   - Implement energy efficiency programs
   - Provide incentives for clean energy adoption
   - Develop long-term energy security strategy

5. **International Cooperation**
   - Diversify import sources to reduce dependency on specific regions
   - Develop strategic partnerships with oil-producing nations
   - Invest in overseas oil assets
""")

# Trend Analysis
st.header("📈 Trend Analysis")

# Calculate year-over-year changes
df['Production_Change'] = df['DOMESTIC_CRUDE_OIL_PRODUCTION'].pct_change() * 100
df['Import_Change'] = df['IMPORTS_OF_CRUDE_OIL'].pct_change() * 100

# Recent trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("Recent Production Trend")
    recent_prod = df['Production_Change'].iloc[-5:]
    st.line_chart(recent_prod)

with col2:
    st.subheader("Recent Import Trend")
    recent_imp = df['Import_Change'].iloc[-5:]
    st.line_chart(recent_imp)


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