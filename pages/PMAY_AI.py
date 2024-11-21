import streamlit as st
import pandas as pd
import requests



# Function to fetch AQI data
def get_aqi_data(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
api_key =db_credentials["weatherapi_key"]  # Replace with your WeatherAPI key

# Fetch AQI data for all states
state_aqi_data = []
for state, city in state_city_mapping.items():
    aqi_response = get_aqi_data(city, api_key)
    if aqi_response and "current" in aqi_response and "air_quality" in aqi_response["current"]:
        air_quality = aqi_response["current"]["air_quality"]
        state_aqi_data.append({
            "State": state,
            "City": city,
            "PM2.5 (μg/m3)": air_quality.get("pm2_5", "N/A"),
            "PM10 (μg/m3)": air_quality.get("pm10", "N/A"),
            "CO (μg/m3)": air_quality.get("co", "N/A"),
            "O3 (μg/m3)": air_quality.get("o3", "N/A"),
            "NO2 (μg/m3)": air_quality.get("no2", "N/A"),
            "SO2 (μg/m3)": air_quality.get("so2", "N/A"),
            "US-EPA Index": air_quality.get("us-epa-index", "N/A"),
        })
    else:
        state_aqi_data.append({
            "State": state,
            "City": city,
            "PM2.5 (μg/m3)": "N/A",
            "PM10 (μg/m3)": "N/A",
            "CO (μg/m3)": "N/A",
            "O3 (μg/m3)": "N/A",
            "NO2 (μg/m3)": "N/A",
            "SO2 (μg/m3)": "N/A",
            "US-EPA Index": "N/A",
        })

# Convert data to DataFrame
df = pd.DataFrame(state_aqi_data)

# Sorting data by US-EPA Index for better visualization
df = df[df["US-EPA Index"] != "N/A"]  # Remove any "N/A" values
df["US-EPA Index"] = pd.to_numeric(df["US-EPA Index"])
df = df.sort_values(by="US-EPA Index", ascending=True)

# Displaying the AQI data
st.title("India AQI Dashboard 🌍")
st.write("Real-time Air Quality Index (AQI) across Indian states. Data includes detailed pollutant levels.")

# Metrics for highest and lowest AQI
highest_aqi = df.iloc[-1]
lowest_aqi = df.iloc[0]
st.subheader("Highlights")
col1, col2 = st.columns(2)
col1.metric(label="State with Best Air Quality", value=lowest_aqi["State"], delta=f"US-EPA Index: {lowest_aqi['US-EPA Index']}")
col2.metric(label="State with Worst Air Quality", value=highest_aqi["State"], delta=f"US-EPA Index: {highest_aqi['US-EPA Index']}")

# Bar chart visualization for US-EPA Index
st.subheader("Air Quality Levels by State (US-EPA Index)")
st.bar_chart(data=df, x="State", y="US-EPA Index", use_container_width=True)

# Detailed Table
st.subheader("Detailed Pollutant Data")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
