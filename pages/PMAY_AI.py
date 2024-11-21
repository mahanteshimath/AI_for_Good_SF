import streamlit as st
import pandas as pd
import requests
import altair as alt

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

# WeatherAPI Key
db_credentials = st.secrets["db_credentials"]
api_key = db_credentials["weatherapi_key"]  # Replace with your WeatherAPI key

# Fetch AQI data for all states
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
            "State": state,
            "City": city,
            "PM2.5 (μg/m³)": pm25_value,
            "PM2.5 Category (DEFRA)": defra_category,
            "PM10 (μg/m³)": air_quality.get("pm10", "N/A"),
            "CO (μg/m³)": air_quality.get("co", "N/A"),
            "O3 (μg/m³)": air_quality.get("o3", "N/A"),
            "NO2 (μg/m³)": air_quality.get("no2", "N/A"),
            "SO2 (μg/m³)": air_quality.get("so2", "N/A"),
            "US-EPA Index": air_quality.get("us-epa-index", "N/A"),
        })
    else:
        state_aqi_data.append({
            "State": state,
            "City": city,
            "PM2.5 (μg/m³)": "N/A",
            "PM2.5 Category (DEFRA)": "N/A",
            "PM10 (μg/m³)": "N/A",
            "CO (μg/m³)": "N/A",
            "O3 (μg/m³)": "N/A",
            "NO2 (μg/m³)": "N/A",
            "SO2 (μg/m³)": "N/A",
            "US-EPA Index": "N/A",
        })

# Convert data to DataFrame
df = pd.DataFrame(state_aqi_data)

# Sorting data by PM2.5 for better visualization
df = df[df["PM2.5 (μg/m³)"] != "N/A"]  # Remove any "N/A" values
df["PM2.5 (μg/m³)"] = pd.to_numeric(df["PM2.5 (μg/m³)"])
df = df.sort_values(by="PM2.5 (μg/m³)", ascending=True)

# Displaying the AQI data
st.title("India AQI Dashboard 🌍")
st.write("Real-time Air Quality Index (AQI) across Indian states. Data includes detailed pollutant levels and DEFRA PM2.5 categories.")

# Metrics for highest and lowest PM2.5
highest_pm25 = df.iloc[-1]
lowest_pm25 = df.iloc[0]
st.subheader("Highlights")
col1, col2 = st.columns(2)
col1.metric(label="State with Best Air Quality (PM2.5)", value=lowest_pm25["State"], delta=f"{lowest_pm25['PM2.5 (μg/m³)']} μg/m³")
col2.metric(label="State with Worst Air Quality (PM2.5)", value=highest_pm25["State"], delta=f"{highest_pm25['PM2.5 (μg/m³)']} μg/m³")

df = pd.DataFrame(state_aqi_data)

# Bar chart visualization for PM2.5
st.subheader("PM2.5 Levels by State (μg/m³)")
alt_chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("PM2.5 (μg/m³):Q", title="PM2.5 (μg/m³)"),
        y=alt.Y("State:O", sort="-x", title="State"),
        color=alt.Color("PM2.5 (μg/m³):Q", scale=alt.Scale(scheme="blues")),
        tooltip=["State", "PM2.5 (μg/m³)", "PM2.5 Category (DEFRA)"],
    )
    .properties(width=800, height=500, title="PM2.5 Levels by State")
)

# Display the chart
st.altair_chart(alt_chart, use_container_width=True)

# Detailed Table
st.subheader("Detailed Pollutant Data with DEFRA Categories")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
