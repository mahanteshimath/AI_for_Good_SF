import streamlit as st
import pandas as pd
import plotly.express as px

def create_accident_visualization():
    # Create the data
    data = {
        'State': [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
            'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand',
            'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur',
            'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
            'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura',
            'Uttarakhand', 'Uttar Pradesh', 'West Bengal', 'Andaman & Nicobar Islands',
            'Chandigarh', 'Dadra & Nagar Haveli', 'Daman & Diu', 'Delhi',
            'Jammu & Kashmir', 'Ladakh', 'Lakshadweep', 'Puducherry'
        ],
        '2019': [5949, 117, 1869, 1628, 2906, 159, 4628, 1871, 934, 1046,
                14169, 9335, 13626, 6465, 327, 24, 29, 46, 3186, 1003,
                3890, 125, 21474, 2614, 288, 370, 9272, 2404, 56, 0,
                33, 5, 0, 746, 0, 0, 249],
        '2020': [4830, 60, 1416, 1372, 1831, 130, 3573, 1421, 530, 1028,
                11791, 6518, 12547, 4336, 176, 13, 26, 72, 2003, 918,
                2872, 71, 17751, 2015, 166, 218, 6776, 1837, 28, 0,
                25, 0, 0, 738, 0, 0, 96],
        '2021': [4786, 106, 1460, 1927, 2056, 103, 4350, 1334, 784, 733,
                11507, 8161, 12052, 5078, 99, 48, 38, 82, 2129, 994,
                3385, 79, 18409, 2075, 243, 238, 7155, 1935, 25, 0,
                66, 0, 0, 958, 71, 0, 117],
        '2022': [4931, 48, 1514, 1679, 2303, 206, 4310, 1461, 839, 836,
                12839, 11002, 12471, 5418, 177, 30, 33, 62, 2373, 1051,
                4143, 96, 23387, 2042, 181, 182, 8264, 2444, 45, 0,
                68, 0, 0, 1868, 81, 0, 101]
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Melt the DataFrame for animation
    df_melted = df.melt(id_vars=['State'], 
                       var_name='Year', 
                       value_name='Injuries')

    # Create the visualization
    st.title('Road Accidents Injuries on State Highways (2019-2022)')

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

    # Add summary statistics
    st.subheader('Summary Statistics')
    yearly_totals = pd.DataFrame({
        'Year': ['2019', '2020', '2021', '2022'],
        'Total Injuries': [110843, 87184, 92583, 106485]
    })
    
    st.write("Yearly Totals:")
    st.dataframe(yearly_totals)

    # Calculate and display key insights
    st.subheader('Key Insights')
    col1, col2 = st.columns(2)
    
    with col1:
        max_state = df_melted.groupby('State')['Injuries'].mean().idxmax()
        max_injuries = df_melted.groupby('State')['Injuries'].mean().max()
        st.metric("State with Highest Average Injuries", max_state, f"{max_injuries:.0f}")
    
    with col2:
        percent_change = ((yearly_totals.iloc[-1,1] - yearly_totals.iloc[0,1]) / 
                         yearly_totals.iloc[0,1] * 100)
        st.metric("Change 2019 to 2022", f"{percent_change:.1f}%")
create_accident_visualization()
