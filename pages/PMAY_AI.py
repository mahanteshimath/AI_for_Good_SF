import streamlit as st
import pandas as pd
import requests
import plotly.express as px


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
            "US-EPA Index": air_quality.get("us-epa-index", "N/A"),
        })
    else:
        state_aqi_data.append({
            "State": state,
            "City": city,
            "US-EPA Index": "N/A",
        })

# Convert data to DataFrame
df = pd.DataFrame(state_aqi_data)

# Clean and categorize data
df = df[df["US-EPA Index"] != "N/A"]  # Remove "N/A" values
df["US-EPA Index"] = pd.to_numeric(df["US-EPA Index"])
df["Air Quality"] = df["US-EPA Index"].map({
    1: "Good",
    2: "Moderate",
    3: "Unhealthy for Sensitive Groups",
    4: "Unhealthy",
    5: "Very Unhealthy",
    6: "Hazardous"
})

# Assign colors for heatmap
color_scale = {
    "Good": "green",
    "Moderate": "yellow",
    "Unhealthy for Sensitive Groups": "orange",
    "Unhealthy": "red",
    "Very Unhealthy": "purple",
    "Hazardous": "maroon",
}

df["Color"] = df["Air Quality"].map(color_scale)

# Display the AQI data
st.title("India AQI Heatmap 🌍")
st.write("Real-time Air Quality Index (AQI) across Indian states based on US-EPA standards.")

# Heatmap visualization
fig = px.choropleth(
    df,
    locationmode="country names",
    locations="State",
    color="Air Quality",
    title="Air Quality Levels Across India",
    color_discrete_map=color_scale,
    scope="asia",
    labels={"Air Quality": "US-EPA Standard"},
)

fig.update_geos(
    visible=False,
    resolution=50,
    showcountries=True,
    countrycolor="Black",
    showcoastlines=True,
    coastlinecolor="LightGray",
)

st.plotly_chart(fig, use_container_width=True)

# Detailed Table
st.subheader("Detailed US-EPA Data")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
