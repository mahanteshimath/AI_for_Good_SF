import streamlit as st
import streamlit.components.v1 as components



# Load the HTML content from the file
with open("./src/Architectureembed.txt", "r") as file:
    html_content = file.read()


st.markdown("[⭐Please give star to motivate](https://github.com/mahanteshimath/AI_for_Good_SF/stargazers)", unsafe_allow_html=True)
# Display the HTML content as an embedded diagram in Streamlit
components.html(html_content, width=800, height=600)

st.markdown('''

This architecture diagram titled **"INDIAN-INFRA-AI-INSIGHTS"** illustrates a data processing and analytics pipeline leveraging Snowflake, data sources, document processing, and a front-end interface using Streamlit. Here's a breakdown of each component and data flow:

1.**Data Sources**
   - **Snowflake Data Marketplace**: Sources datasets related to infrastructure, weather, and other public data.
   - **data.gov.in**: Provides open government datasets for analysis.
   - **Custom Datasets**: Uploads from external sources are processed into Snowflake for analysis.
   - **Weather API**: Fetches Air Quality Index (AQI) data and other weather-related metrics.

2. **Snowflake Database (Snowflake DB)**:
   - **Data Ingestion and Processing**: All data sources are ingested into Snowflake, where the data is stored and processed. This includes cleaning, transforming, and preparing the data for analysis. The processed data is saved in **final views** or **functions** within Snowflake.
   - These views and functions represent structured, ready-to-use datasets for downstream analysis or embedding into the application.

3. **Data Processing and Embedding for Analysis**:
   - **Documents**: This section represents document-based data (PDFs, Word files, etc.), which is **extracted and chunked** into manageable parts. These chunks are processed to create **embeddings**—vector representations of the data, which can be used in machine learning or AI applications for similarity search, natural language processing, or other analyses.
   - **Vector Store**: The embeddings are stored in a vector database. This enables quick retrieval based on similarity and facilitates advanced AI-driven queries on the data.

4. **Data Delivery to Streamlit**:
   - **Streamlit**: The processed data and insights are visualized in a front-end interface using Streamlit, a popular Python framework for creating interactive web apps for data science and machine learning applications. Streamlit allows users to explore and interact with the insights generated from the processed data.

5. **Data Flow**:
   - The arrows in the diagram represent data flow between these components. Data moves from data sources to the Snowflake DB, undergoes transformation and embedding, and is then either stored in the vector store for AI applications or made directly available for visualization in Streamlit.

### Key Points:
- **Purpose**: The architecture is designed to facilitate **data-driven insights** and AI applications, with Snowflake as the core data warehouse and Streamlit as the visualization layer.
- **Processing Steps**: Data is sourced, processed, embedded (if required), and visualized, making it suitable for interactive exploration or advanced AI tasks.
- **Scalability**: The use of Snowflake and vector stores suggests a scalable solution, capable of handling large datasets and complex AI-driven analyses. 

This architecture is suitable for data-driven applications focusing on infrastructure or government-related analytics in India, leveraging AI and visualization tools to generate actionable insights.

''')

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