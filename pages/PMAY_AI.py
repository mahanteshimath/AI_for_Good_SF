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
api_key =db_credentials["weatherapi_key"]  # Replace with your WeatherAPI key

# Fetch AQI data for all states
state_aqi_data = []
for state, city in state_city_mapping.items():
    aqi_response = get_aqi_data(city, api_key)
    if aqi_response and "current" in aqi_response:
        aqi = aqi_response["current"]["air_quality"]["us-epa-index"]
        state_aqi_data.append({"State": state, "City": city, "AQI": aqi})
    else:
        state_aqi_data.append({"State": state, "City": city, "AQI": "N/A"})

# Convert data to DataFrame
df = pd.DataFrame(state_aqi_data)

# Sorting data for better visualization
df = df[df["AQI"] != "N/A"]  # Remove any "N/A" values
df["AQI"] = pd.to_numeric(df["AQI"])
df = df.sort_values(by="AQI", ascending=True)

# Displaying the AQI data
st.title("India AQI Dashboard 🌍")
st.write("Real-time Air Quality Index (AQI) across Indian states.")

# Metrics for highest and lowest AQI
highest_aqi = df.iloc[-1]
lowest_aqi = df.iloc[0]
st.subheader("Highlights")
col1, col2 = st.columns(2)
col1.metric(label="State with Best AQI", value=lowest_aqi["State"], delta=f"AQI: {lowest_aqi['AQI']}")
col2.metric(label="State with Worst AQI", value=highest_aqi["State"], delta=f"AQI: {highest_aqi['AQI']}")

# Bar chart visualization
st.subheader("AQI Levels by State")
st.bar_chart(data=df, x="State", y="AQI", use_container_width=True)

# Detailed Table
st.subheader("Detailed AQI Data")
st.dataframe(df.reset_index(drop=True), use_container_width=True)


