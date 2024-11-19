import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Expanded Indian Cities List
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", 
    "Hyderabad", "Pune", "Ahmedabad", "Surat", "Jaipur",
    "Lucknow", "Bhopal", "Patna", "Indore", "Chandigarh", 
    "Thiruvananthapuram", "Guwahati", "Bhubaneswar", "Ranchi", "Nagpur"
]

# Weather API Configuration
WEATHERAPI_KEY = st.session_state.weatherapi_key 

def get_weather_data(city):
    weather_url = f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_KEY}&q={city}"
    try:
        response = requests.get(weather_url)
        return response.json()
    except Exception as e:
        st.error(f"Weather Data Error: {e}")
        return None

def get_forecast_data(city):
    forecast_url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_KEY}&q={city}&days=7"
    try:
        response = requests.get(forecast_url)
        return response.json()
    except Exception as e:
        st.error(f"Forecast Data Error: {e}")
        return None
    st.set_page_config(page_title="India Weather Dashboard", layout="wide")
    st.title("🌍 Comprehensive Weather & Climate Dashboard")
    
    # City Selection with Enhanced Options
    col1, col2 = st.columns(2)
    
    with col1:
        selected_city = st.selectbox("Select City", INDIAN_CITIES, index=0)
    
    with col2:
        weather_type = st.radio("View Type", 
            ["Current Weather", "7-Day Forecast", "Climate Details"]
        )
    
    # Data Retrieval
    weather_data = get_weather_data(selected_city)
    forecast_data = get_forecast_data(selected_city)
    
    if weather_data and forecast_data:
        # Current Weather Section
        if weather_type == "Current Weather":
            st.subheader(f"🌡️ Current Weather in {selected_city}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Temperature", f"{weather_data['current']['temp_c']}°C")
                st.metric("Feels Like", f"{weather_data['current']['feelslike_c']}°C")
            
            with col2:
                st.metric("Humidity", f"{weather_data['current']['humidity']}%")
                st.metric("Wind Speed", f"{weather_data['current']['wind_kph']} km/h")
            
            with col3:
                st.metric("Precipitation", f"{weather_data['current']['precip_mm']} mm")
                st.metric("UV Index", str(weather_data['current']['uv']))
            
            # Condition Visualization
            condition = weather_data['current']['condition']['text']
            st.write(f"**Current Condition:** {condition}")
        
        # 7-Day Forecast
        elif weather_type == "7-Day Forecast":
            st.subheader(f"🌈 7-Day Weather Forecast for {selected_city}")
            
            forecast_df = pd.DataFrame([
                {
                    'Date': day['date'], 
                    'Max Temp (°C)': day['day']['maxtemp_c'],
                    'Min Temp (°C)': day['day']['mintemp_c'],
                    'Condition': day['day']['condition']['text']
                } for day in forecast_data['forecast']['forecastday']
            ])
            
            fig = px.line(forecast_df, x='Date', y=['Max Temp (°C)', 'Min Temp (°C)'], 
                          title='Temperature Trend')
            st.plotly_chart(fig)
            
            st.dataframe(forecast_df)
        
        # Climate Details
        else:
            st.subheader(f"🌍 Climate Overview for {selected_city}")
            
            climate_data = {
                'Average Max Temp': forecast_data['forecast']['forecastday'][0]['day']['maxtemp_c'],
                'Average Min Temp': forecast_data['forecast']['forecastday'][0]['day']['mintemp_c'],
                'Total Precipitation': forecast_data['forecast']['forecastday'][0]['day']['totalprecip_mm'],
                'Max Wind Speed': weather_data['current']['wind_kph']
            }
            
            for key, value in climate_data.items():
                st.metric(key, str(value))
            
            # Radar Chart for Climate Parameters
            fig = go.Figure(data=[go.Scatterpolar(
                r=[climate_data['Average Max Temp'], 
                   climate_data['Average Min Temp'], 
                   climate_data['Total Precipitation'], 
                   climate_data['Max Wind Speed']],
                theta=['Max Temp', 'Min Temp', 'Precipitation', 'Wind Speed'],
                fill='toself'
            )])
            fig.update_layout(title='Climate Radar')
            st.plotly_chart(fig)
