import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time



st.logo(
    image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
    link="https://www.linkedin.com/in/mahantesh-hiremath/",
    icon_image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
)
words = ["INDIAN", "INFRA", "AI", "INSIGHTS"]
with st.container():
    # Placeholder for word rotation
    placeholder = st.empty()

    # Infinite loop for rotating words
    while True:
        for word in words:
            # Display each word in bold and centered style
            placeholder.markdown(
                f"<h1 style='text-align: center; font-size: 3em; font-weight: bold;'>{word}</h1>",
                unsafe_allow_html=True
            )
            time.sleep(1)  


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
st.markdown("""---------------------------------""")
st.write("\n")

st.write("\n")
st.title("Girish Bharadwaj: Bridge Man of India")


article_content = """
### Girish Bharadwaj: How a Hole in a Boat Led to the Emergence of Bridge Man of India
*(Excerpt from The New Indian Express)*

Girish Bharadwaj, known as the "Bridge Man of India," has transformed rural connectivity in India by building over 130 bridges across various states, including Karnataka, Kerala, Telangana, and Odisha. His journey began in 1989 when residents of Aramburu village, tired of relying on a boat that frequently broke down, approached him to construct a footbridge. Despite being a mechanical engineer with no prior experience in bridge construction, Bharadwaj was inspired by the villagers' determination and decided to help.

He designed a low-cost hanging bridge with assistance from engineering friends and local villagers, completing the project for under ₹2 lakh. This initial success led to government collaboration, expanding his efforts to connect isolated communities. Bharadwaj's bridges are notable for their cost-effectiveness and durability, often surpassing their intended lifespan of 10-20 years.

His innovative approach draws inspiration from famous suspension bridges like San Francisco's Golden Gate Bridge while adapting designs to local needs. He has received recognition for his contributions, including the Padma Shri award in 2017. Now, his son continues his legacy as demand shifts towards larger structures due to increased vehicle use. Bharadwaj’s work not only improved infrastructure but also empowered rural communities by connecting them to broader opportunities.

...

For more details, please refer to the [full article on The New Indian Express](https://www.newindianexpress.com/good-news/2020/Nov/15/girish-bharadwajhow-a-hole-in-a-boat-led-to-the-emergence-of-bridge-man-of-india-2223737.html).
"""

st.markdown(article_content)

st.markdown("""---------------------------------""")

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
