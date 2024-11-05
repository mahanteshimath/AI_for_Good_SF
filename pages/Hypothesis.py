import streamlit as st

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
st.subheader("Experience & Qualifications", anchor=False)
st.write(
    """
    - 7 Years experience extracting actionable insights from data
    - Strong hands-on experience and knowledge in Python and Excel
    - Good understanding of statistical principles and their respective applications
    - Excellent team-player and displaying a strong sense of initiative on tasks
    """
)
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Programming: Python (Scikit-learn, Pandas), SQL, VBA
    - Data Visualization: PowerBi, MS Excel, Plotly
    - Modeling: Logistic regression, linear regression, decision trees
    - Databases: Postgres, MongoDB, MySQL
    """
)
