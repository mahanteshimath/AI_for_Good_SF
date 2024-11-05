import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
        '''Giving more focus on infra development lead to overall country development in all angles best examples are Dubai and Singapore. We can learn from proven strategies and implementing them with productively will help to India to become developed country.
   Leveraging AI-driven analytics for urban infrastructure such as predictive maintenance, public transport optimization, energy forecasting, smart waste management, disaster resilience, and affordable housing can greatly enhance sustainability and quality of life in Indian megacities.'''
    )
    st.write("\n")
    st.write(
        '''Finally my point is sometimes building one bridge helped villages to improve economically i.e people can transport goods or youth can go for jobs or higher education.'''
    )

st.write("\n")

st.write("\n")



# Creating the budget allocation data as a DataFrame
data = {
    "Financial Year": [
        "1999-2000", "2004-05", "2009-10", "2014-15", 
        "2019-20", "2020-21", "2021-22", "2022-23", 
        "2023-24", "2024-25"
    ],
    "Budget Allocation (in lakh crore)": [
        0.55, 0.87, 1.0, 1.75, 
        3.38, 4.39, 5.54, 7.5, 
        10.0, 11.11
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

# Convert the data to a DataFrame
df = pd.DataFrame(data)


# df = pd.read_csv('src/InfraBudget.csv')

# Set the title of the app
st.title("Budget Allocation Over Financial Years")

r1_expander = st.expander("Budget Allocation Data")
r1_expander.table(df)
plt.figure(figsize=(8, 6))
bars = plt.bar(df["Financial Year"], df["Budget Allocation (in lakh crore)"], color='skyblue')
plt.title("Budget Allocation (in lakh crore) by Financial Year")
plt.xlabel("Financial Year")
plt.ylabel("Budget Allocation (in lakh crore)")
plt.xticks(rotation=45)
plt.grid(axis='y')

# Add values on top of the bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), ha='center', va='bottom')

# Display the chart in Streamlit
st.pyplot(plt)
