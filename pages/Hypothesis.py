import streamlit as st
import pandas as pd
import plotly.express as px
st.logo(
    image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
    link="https://www.linkedin.com/in/mahantesh-hiremath/",
    icon_image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
)

col1, col2 = st.columns(2, gap="small")
with col1:
    st.image("./src/India.jpeg")

with col2:
    st.title("Hypothesis", anchor=False)
    st.write(
        "Senior Data Analyst, assisting enterprises by supporting data-driven decision-making."
    )

st.write("\n")
# st.subheader("Experience & Qualifications", anchor=False)
# st.write(
#     """
#     - 7 Years experience extracting actionable insights from data
#     - Strong hands-on experience and knowledge in Python and Excel
#     - Good understanding of statistical principles and their respective applications
#     - Excellent team-player and displaying a strong sense of initiative on tasks
#     """
# )
st.write("\n")



# Define the data
data = {
    "Financial Year": [
        "1999-2000", "2004-05", "2009-10", "2014-15", "2019-20", 
        "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"
    ],
    "Budget Allocation (in ₹ lakh crore)": [
        0.55, 0.87, 1.0, 1.75, 3.38, 
        4.39, 5.54, 7.5, 10.0, 11.11
    ],
    "Notes": [
        "Initial allocations for infrastructure projects.",
        "Increase due to focus on rural and urban infrastructure.",
        "Global financial crisis prompted increased spending.",
        "Significant push under the new government.",
        "Continued emphasis on infrastructure as part of economic growth strategy.",
        "Response to COVID-19 with a focus on economic recovery.",
        "Increased investment in roads, railways, and urban development.",
        "Major projects in transportation and housing initiated.",
        "Strong focus on sustainable infrastructure and green projects.",
        "Marked increase to support extensive infrastructure initiatives across sectors."
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Display the title
st.title("Infrastructure Budget Allocation in India (1999-2025)")

# Plot a bar chart with Plotly
fig = px.bar(
    df, 
    x="Financial Year", 
    y="Budget Allocation (in ₹ lakh crore)", 
    text="Budget Allocation (in ₹ lakh crore)",
    hover_data={"Financial Year": True, "Budget Allocation (in ₹ lakh crore)": True, "Notes": True},
    labels={"Budget Allocation (in ₹ lakh crore)": "Budget Allocation (₹ lakh crore)"},
    title="India's Infrastructure Budget Allocation Over the Years"
)

# Customize the chart
fig.update_traces(
    texttemplate='%{text:.2s}', 
    textposition='outside',
    marker_color='royalblue'
)
fig.update_layout(
    yaxis_title="Budget Allocation (in ₹ lakh crore)",
    xaxis_title="Financial Year",
    hoverlabel=dict(bgcolor="blue", font_size=12, font_family="Arial"),
    template="plotly_white"
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

# Display the notes below the chart as a table for easy reference
st.subheader("Detailed Notes for Each Year")
st.table(df[["Financial Year", "Notes"]])
