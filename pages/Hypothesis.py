import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
st.title("India's Infrastructure Budget Allocation (1999-2025)")

# Plot with Plotly Graph Objects
fig = go.Figure()

# Add bar chart
fig.add_trace(go.Bar(
    x=df["Financial Year"],
    y=df["Budget Allocation (in ₹ lakh crore)"],
    text=df["Budget Allocation (in ₹ lakh crore)"],
    marker=dict(
        color=df["Budget Allocation (in ₹ lakh crore)"],
        colorscale="Viridis",
        showscale=True
    ),
    texttemplate='%{text:.2f}',
    textposition='outside',
    name="Budget Allocation"
))

# Add trend line
fig.add_trace(go.Scatter(
    x=df["Financial Year"], 
    y=df["Budget Allocation (in ₹ lakh crore)"], 
    mode="lines+markers",
    line=dict(color="crimson", width=2, dash="dash"),
    name="Trend Line"
))

# Annotate significant years
annotations = [
    dict(
        x="2009-10", y=1.0, 
        text="Global Financial Crisis - Increased Spending",
        showarrow=True, arrowhead=1, ax=-40, ay=-80
    ),
    dict(
        x="2014-15", y=1.75, 
        text="New Government Infrastructure Push",
        showarrow=True, arrowhead=1, ax=-40, ay=-80
    ),
    dict(
        x="2020-21", y=4.39, 
        text="COVID-19 Economic Recovery",
        showarrow=True, arrowhead=1, ax=-40, ay=-80
    ),
    dict(
        x="2023-24", y=10.0, 
        text="Focus on Sustainable & Green Projects",
        showarrow=True, arrowhead=1, ax=-40, ay=-80
    )
]
fig.update_layout(annotations=annotations)

# Customize the layout
fig.update_layout(
    title="Growth in India's Infrastructure Budget Allocation Over the Years",
    xaxis_title="Financial Year",
    yaxis_title="Budget Allocation (in ₹ lakh crore)",
    template="plotly_white",
    coloraxis_colorbar=dict(
        title="Budget (₹ lakh crore)"
    ),
    yaxis=dict(tickformat=","),
    hovermode="x unified",
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig)

# Display the notes below the chart as a table for easy reference
st.subheader("Detailed Notes for Each Year")
st.table(df[["Financial Year", "Budget Allocation (in ₹ lakh crore)","Notes"]])
