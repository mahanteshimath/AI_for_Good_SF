import streamlit as st
import pandas as pd
import requests
import altair as alt
import snowflake.connector

# Function to fetch AQI data
def get_aqi_data(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to categorize PM2.5 levels based on DEFRA Index
def categorize_pm25_defra(pm25_value):
    if pm25_value <= 11:
        return "Low (1)"
    elif pm25_value <= 23:
        return "Low (2)"
    elif pm25_value <= 35:
        return "Low (3)"
    elif pm25_value <= 41:
        return "Moderate (4)"
    elif pm25_value <= 47:
        return "Moderate (5)"
    elif pm25_value <= 53:
        return "Moderate (6)"
    elif pm25_value <= 58:
        return "High (7)"
    elif pm25_value <= 64:
        return "High (8)"
    elif pm25_value <= 70:
        return "High (9)"
    else:
        return "Very High (10)"

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

# Create Snowflake table
def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS T01_AQI_FOR_INDIAN_STATES (
        State VARCHAR,
        City VARCHAR,
        PM25 FLOAT,
        PM25_Category VARCHAR,
        PM10 FLOAT,
        CO FLOAT,
        O3 FLOAT,
        NO2 FLOAT,
        SO2 FLOAT,
        US_EPA_Index FLOAT,
        INSRT_TIMESTAMP TIMESTAMP_NTZ DEFAULT CONVERT_TIMEZONE('Asia/Kolkata', CURRENT_TIMESTAMP)
    )
    """
    execute_query(create_table_query)

# Insert data into Snowflake
def insert_data_to_snowflake(dataframe):
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
        insert_query = """
        INSERT INTO T01_AQI_FOR_INDIAN_STATES (
            State, City, PM25, PM25_Category, PM10, CO, O3, NO2, SO2, US_EPA_Index
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        for _, row in dataframe.iterrows():
            cursor.execute(insert_query, (
                row["State"], row["City"], row["PM2.5 (μg/m³)"],
                row["PM2.5 Category (DEFRA)"], row["PM10 (μg/m³)"],
                row["CO (μg/m³)"], row["O3 (μg/m³)"], row["NO2 (μg/m³)"],
                row["SO2 (μg/m³)"], row["US-EPA Index"]
            ))
        conn.commit()
        st.success("Data pushed to Snowflake successfully.")
        conn.close()
    except Exception as e:
        st.error(f"Error inserting data to Snowflake: {str(e)}")


# List of Indian states and their representative cities
state_city_mapping = {
    "Andhra Pradesh": "Vijayawada",
    "Arunachal Pradesh": "Itanagar",
    "Assam": "Guwahati",
    "Bihar": "Patna",
    "Chhattisgarh": "Raipur",
    "Delhi": "New Delhi",
    "Goa": "Panaji",
    "Gujarat": "Ahmedabad",
    "Haryana": "Chandigarh",
    "Himachal Pradesh": "Shimla",
    "Jharkhand": "Ranchi",
    "Karnataka": "Bengaluru",
    "Kerala": "Thiruvananthapuram",
    "Madhya Pradesh": "Bhopal",
    "Maharashtra": "Mumbai",
    "Manipur": "Imphal",
    "Meghalaya": "Shillong",
    "Mizoram": "Aizawl",
    "Nagaland": "Kohima",
    "Odisha": "Bhubaneswar",
    "Punjab": "Amritsar",
    "Rajasthan": "Jaipur",
    "Sikkim": "Gangtok",
    "Tamil Nadu": "Chennai",
    "Telangana": "Hyderabad",
    "Tripura": "Agartala",
    "Uttar Pradesh": "Lucknow",
    "Uttarakhand": "Dehradun",
    "West Bengal": "Kolkata",
}

# API Key
db_credentials = st.secrets["db_credentials"]
api_key = db_credentials["weatherapi_key"]

# Fetch AQI data
state_aqi_data = []
for state, city in state_city_mapping.items():
    aqi_response = get_aqi_data(city, api_key)
    if aqi_response and "current" in aqi_response and "air_quality" in aqi_response["current"]:
        air_quality = aqi_response["current"]["air_quality"]
        pm25_value = air_quality.get("pm2_5", "N/A")
        if pm25_value != "N/A":
            pm25_value = float(pm25_value)
            defra_category = categorize_pm25_defra(pm25_value)
        else:
            defra_category = "N/A"
        state_aqi_data.append({
            "State": state, "City": city, "PM2.5 (μg/m³)": pm25_value,
            "PM2.5 Category (DEFRA)": defra_category,
            "PM10 (μg/m³)": air_quality.get("pm10", "N/A"),
            "CO (μg/m³)": air_quality.get("co", "N/A"),
            "O3 (μg/m³)": air_quality.get("o3", "N/A"),
            "NO2 (μg/m³)": air_quality.get("no2", "N/A"),
            "SO2 (μg/m³)": air_quality.get("so2", "N/A"),
            "US-EPA Index": air_quality.get("us-epa-index", "N/A"),
        })

# Convert to DataFrame
df = pd.DataFrame(state_aqi_data)
df = df[df["PM2.5 (μg/m³)"] != "N/A"]
df["PM2.5 (μg/m³)"] = pd.to_numeric(df["PM2.5 (μg/m³)"])

# Visualization
st.title("India AQI Dashboard 🌍")
st.write("Real-time Air Quality Index (AQI) across Indian states.")

st.subheader("Refresh data from weatherapi ")
if st.button("Push Data to snowflake"):
    create_table()
    insert_data_to_snowflake(df)


Q1=f'''SELECT * FROM T01_AQI_FOR_INDIAN_STATES'''
R1 = execute_query(Q1)
r1_expander = st.expander("Data sets used in this entire analysis.")
R1_DF = pd.DataFrame(R1)
R1_DF.index = R1_DF.index + 1
r1_expander.write(R1_DF)

df=R1_DF

# Custom CSS
st.markdown("""
    <style>
    .metric-container {
        display: flex;
        gap: 1rem;
        justify-content: space-around;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: black;
        border: 3px solid #ddd;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        width: 150px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease-in-out;
;
    }
    </style>
""", unsafe_allow_html=True)

# Default Values
default_state = "Andhra Pradesh"
default_city = "Vijayawada"

# Sidebar Filters
state_filter = st.selectbox("Select State", df["STATE"].unique(), index=df["STATE"].unique().tolist().index(default_state))

# Filter Data
filtered_data = df[(df["STATE"] == state_filter)]


if not filtered_data.empty:
    # Metrics Section
    latest_entry = filtered_data.iloc[-1]
    st.subheader(f"Air Quality Metrics for  {state_filter}")
    
    metric_html = f"""
        <div class="metric-container">
            <div class="metric-box"><strong>PM2.5</strong><br>{latest_entry['PM25']}<br><small>{latest_entry['PM25_CATEGORY']}</small></div>
            <div class="metric-box"><strong>PM10</strong><br>{latest_entry['PM10']}</div>
            <div class="metric-box"><strong>US EPA Index</strong><br>{latest_entry['US_EPA_INDEX']}</div>
            <div class="metric-box"><strong>CO</strong><br>{latest_entry['CO']}</div>
            <div class="metric-box"><strong>O3</strong><br>{latest_entry['O3']}</div>
            <div class="metric-box"><strong>NO2</strong><br>{latest_entry['NO2']}</div>
            <div class="metric-box"><strong>SO2</strong><br>{latest_entry['SO2']}</div>
        </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)
    
    # Historical Data Table
    st.write("### Historical Data")
    st.dataframe(filtered_data)
    
    # Visualizations
    st.write("### Visualizations")
    st.line_chart(filtered_data.set_index("INSRT_TIMESTAMP")[["PM25", "PM10", "CO", "O3", "NO2", "SO2"]])
else:
    st.warning("No data available for the selected filters.")