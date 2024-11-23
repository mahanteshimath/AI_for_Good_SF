import streamlit as st
import snowflake.connector
from datetime import datetime
import pytz





# Custom theme configuration
st.markdown("""
    <style>
        /* Global styles */
        .stApp {
            background-color: #2f1f42;
        }
        
        /* Main container styling */
        .main {
            background-color: #2f1f42;
            color: #c7e5b0;
        }
        
        /* Card styling */
        .stCard {
            background-color: #220e06;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-bottom: 1rem;
            border: 1px solid #cebde0;
        }
        
        /* Header styling */
        .main-header {
            color: #cebde0;
            font-size: 2.5rem;
            font-weight: 800;
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #cebde0;
        }
        
        .section-header {
            color: #cebde0;
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #cebde0;
        }
        
        /* Label styling */
        .stSelectbox label, .stNumberInput label, .stTextInput label {
            color: #c7e5b0 !important;
            font-weight: 600;
            font-size: 1rem;
        }
        
        /* Input field styling */
        .stSelectbox > div > div, .stNumberInput > div > div, .stTextInput > div {
            background-color: #2f1f42 !important;
            border-radius: 0.5rem;
            border: 2px solid #cebde0 !important;
            color: #c7e5b0 !important;
            font-weight: 500;
        }
        
        .stSelectbox > div > div:hover, .stNumberInput > div > div:hover, .stTextInput > div:hover {
            border-color: #cebde0 !important;
            box-shadow: 0 0 0 1px #cebde0;
        }
        
        /* Dropdown styling */
        .stSelectbox > div > div > div[data-baseweb="select"] > div {
            background-color: #2f1f42 !important;
            color: #c7e5b0 !important;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #cebde0;
            color: #2f1f42;
            font-weight: 700;
            padding: 0.75rem 2rem;
            border-radius: 0.5rem;
            border: none;
            width: 100%;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .stButton > button:hover {
            background-color: #c7e5b0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        /* Success/Error message styling */
        .element-container .stSuccess {
            background-color: #220e06;
            color: #c7e5b0;
            border: 2px solid #c7e5b0;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            font-weight: 600;
        }
        
        .element-container .stError {
            background-color: #220e06;
            color: #ff6b6b;
            border: 2px solid #ff6b6b;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            font-weight: 600;
        }
        
        /* Input text color */
        input, textarea, [data-baseweb="select"] {
            color: #c7e5b0 !important;
        }
        
        /* Dropdown menu styling */
        [data-baseweb="popover"] {
            background-color: #2f1f42 !important;
        }
        
        [data-baseweb="menu"] {
            background-color: #2f1f42 !important;
        }
        
        [data-baseweb="option"] {
            color: #c7e5b0 !important;
        }
        
        [data-baseweb="option"]:hover {
            background-color: #220e06 !important;
        }
        
        /* Number input arrows */
        input[type="number"] {
            color: #c7e5b0 !important;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 10px;
            background: #2f1f42;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #cebde0;
            border-radius: 5px;
        }
        
        /* Responsive layout */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
            }
            
            .stCard {
                padding: 1rem;
            }
        }
    </style>
""", unsafe_allow_html=True)





# Add new CSS for the results card
st.markdown("""
    <style>
        /* Existing CSS remains the same */
        
        /* Results card styling */
        .results-card {
            background-color: #220e06;
            padding: 2rem;
            border-radius: 1rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            margin-top: 2rem;
            border: 2px solid #c7e5b0;
        }
        
        .results-header {
            color: #cebde0;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        .result-item {
            color: #c7e5b0;
            font-size: 1.2rem;
            margin-bottom: 1rem;
            padding: 0.5rem;
            border-bottom: 1px solid #cebde0;
        }
        
        .probability-high {
            color: #ff6b6b;
        }
        
        .probability-medium {
            color: #ffd93d;
        }
        
        .probability-low {
            color: #6bff6b;
        }
    </style>
""", unsafe_allow_html=True)
# Main header
st.markdown('<h1 class="main-header">Road Accidents Prediction and Prevention Using AI</h1>', unsafe_allow_html=True)

# Initialize connection to Snowflake
def init_connection():
    return snowflake.connector.connect(
            account=st.session_state.account,
            role=st.session_state.role,
            warehouse=st.session_state.warehouse,
            database=st.session_state.database,
            schema=st.session_state.schema,
            user=st.session_state.user,
            password=st.session_state.password,
            client_session_keep_alive=True
    )

# Function to insert data into Snowflake
def insert_data(data):
    conn = init_connection()
    cur = conn.cursor()
    
    query = """
    INSERT INTO T01_ROAD_ACCIDENTS (
        VEHICLE_NUMBER, ROAD_SURFACE_CONDITIONS, WEATHER_CONDITIONS, 
        LIGHT_CONDITIONS, NUMBER_OF_VEHICLES, ROAD_TYPE, 
        URBAN_OR_RURAL_AREA, VEHICLE_TYPE, DRIVER_AGE,
        DRIVER_SEX, DRIVER_HOME_AREA_TYPE, VEHICLE_AGE,
        SPEED_LIMIT, JUNCTION_DETAIL, JUNCTION_CONTROL,
        PEDESTRIAN_CROSSING_HUMAN_CONTROL, PEDESTRIAN_CROSSING_PHYSICAL_FACILITIES,
        ROAD_CLASS, TIME_OF_DAY
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cur.execute(query, (
        data["vehicle_number"], data["road_surface"], data["weather"],
        data["light"], data["num_vehicles"], data["road_type"],
        data["area"], data["vehicle_type"], data["driver_age"],
        data["driver_sex"], data["home_area"], data["vehicle_age"],
        data["speed_limit"], data["junction_detail"], data["junction_control"],
        data["ped_control"], data["ped_facilities"], data["road_class"],
        data["time_of_day"]
    ))

    query_upd = """UPDATE T01_ROAD_ACCIDENTS TGT
    SET 
        TGT.ACCIDENT_PROBABILITY=SRC.PREDICTED_ACCIDENT_PROBABILITY,
        TGT.ACCIDENT_SEVERITY=SRC.PREDICTED_SEVERITY,
        TGT.OUTPUT=SRC.OUTPUT
    FROM V01_PREDICTED_DATA SRC
    WHERE SRC.VEHICLE_NUMBER = TGT.VEHICLE_NUMBER AND SRC.INSRT_TIMESTAMP=SRC.INSRT_TIMESTAMP;
    """
    cur.execute(query_upd)
    conn.commit()
    cur.close()
    conn.close()



# Function to get prediction results
def get_prediction_results(vehicle_number):
    conn = init_connection()
    cur = conn.cursor()
    
    query = """
    SELECT VEHICLE_NUMBER, INSRT_TIMESTAMP, ACCIDENT_PROBABILITY, 
           ACCIDENT_SEVERITY, OUTPUT 
    FROM T01_ROAD_ACCIDENTS 
    WHERE (VEHICLE_NUMBER, INSRT_TIMESTAMP) IN (
        SELECT VEHICLE_NUMBER, MAX(INSRT_TIMESTAMP) INSRT_TIMESTAMP  
        FROM T01_ROAD_ACCIDENTS 
        WHERE VEHICLE_NUMBER = %s 
        GROUP BY ALL
    )
    """
    
    cur.execute(query, (vehicle_number,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    
    return result

    # Function to parse percentage string
def parse_percentage(percentage_str):
    if isinstance(percentage_str, str):
        # Remove the % symbol and convert to float
        return float(percentage_str.strip('%'))
    return float(percentage_str)




# Create three columns with cards
col1, col2, col3 = st.columns(3)

# ROAD CONDITIONS
with col1:
    # st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Road Conditions</h2>', unsafe_allow_html=True)
    
    vehicle_number = st.text_input("Vehicle Number", key="vehicle_number")
    
    road_surface = st.selectbox(
        "Road Surface Conditions",
        ["Dry", "Wet", "Snow", "Ice", "Flood", "Mud"]
    )
    
    road_type = st.selectbox(
        "Road Type",
        ["Motorway", "Dual Carriageway", "Single Carriageway", "Roundabout", "Traffic Calmed", "Urban Road"]
    )
    
    road_class = st.selectbox(
        "Road Class",
        ["Motorway", "A Road", "B Road", "Minor Road", "Restricted Local Access Road"]
    )
    
    area = st.selectbox(
        "Urban or Rural Area",
        ["Urban", "Rural"]
    )
    
    junction_detail = st.selectbox(
        "Junction Detail",
        ["No Junction", "Roundabout", "Mini Roundabout", "T-Junction", "Staggered Junction", "Crossroads"]
    )
    
    junction_control = st.selectbox(
        "Junction Control",
        ["Uncontrolled", "Authorised Person", "Traffic Signals", "Stop Sign", "Give Way"]
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ENVIRONMENTAL CONDITIONS
with col2:
    # st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Environmental Conditions</h2>', unsafe_allow_html=True)
    
    weather = st.selectbox(
        "Weather Conditions",
        ["Clear", "Rainy", "Foggy", "Stormy", "Windy", "Hazy"]
    )
    
    light = st.selectbox(
        "Light Conditions",
        ["Daylight", "Dark - Street Lights On", "Dark - Street Lights Off", "Dusk", "Dawn"]
    )
    
    time_of_day = st.selectbox(
        "Time of Day",
        ["Early Morning", "Morning Rush Hour", "Late Morning", "Afternoon", "Evening Rush Hour", "Night", "Late Night"]
    )
    
    ped_control = st.selectbox(
        "Pedestrian Control",
        ["None", "Pelican Crossing", "Zebra Crossing", "Footbridge", "Underpass"]
    )
    
    ped_facilities = st.selectbox(
        "Pedestrian Crossing Physical Facilities",
        ["None", "Zebra Crossing", "Pelican Crossing", "Footbridge", "Underpass"]
    )
    
    speed_limit = st.number_input("Speed Limit", min_value=0, max_value=120, value=30)
    st.markdown('</div>', unsafe_allow_html=True)

# VEHICLE & DRIVER INFORMATION
with col3:
    # st.markdown('<div class="stCard">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header">Vehicle & Driver Information</h2>', unsafe_allow_html=True)
    
    num_vehicles = st.number_input("Number of Vehicles", min_value=1, max_value=20, value=1)
    
    vehicle_type = st.selectbox(
        "Vehicle Type",
        ["Car", "Motorcycle", "Bus", "Truck", "Van", "Auto-Rickshaw", "Bicycle", "Pedestrian"]
    )
    
    vehicle_age = st.text_input("Vehicle Age")
    
    driver_age = st.number_input("Driver Age", min_value=16, max_value=100, value=30)
    
    driver_sex = st.selectbox(
        "Driver Sex",
        ["Male", "Female", "Other"]
    )
    
    home_area = st.selectbox(
        "Driver Home Area Type",
        ["Residential", "Commercial", "Industrial", "Rural", "Suburban"]
    )
    # st.markdown('</div>', unsafe_allow_html=True)

# Submit button container with styling
st.markdown('<div class="stCard" style="text-align: center;">', unsafe_allow_html=True)
if st.button("Submit Data to get prediction", key="submit"):
    if not vehicle_number:
        st.error("Please enter a vehicle number")
    else:
        data = {
            "vehicle_number": vehicle_number,
            "road_surface": road_surface,
            "weather": weather,
            "light": light,
            "num_vehicles": num_vehicles,
            "road_type": road_type,
            "area": area,
            "vehicle_type": vehicle_type,
            "driver_age": driver_age,
            "driver_sex": driver_sex,
            "home_area": home_area,
            "vehicle_age": vehicle_age,
            "speed_limit": speed_limit,
            "junction_detail": junction_detail,
            "junction_control": junction_control,
            "ped_control": ped_control,
            "ped_facilities": ped_facilities,
            "road_class": road_class,
            "time_of_day": time_of_day
        }
        
        try:
            insert_data(data)
            st.success("Data successfully paased to AI to predict")
            st.balloons()
            prediction_results = get_prediction_results(vehicle_number)
            
            if prediction_results:
                st.markdown('<h3 class="results-header">Prediction Results</h3>', unsafe_allow_html=True)
                
                veh_num, timestamp, probability, severity, output = prediction_results
                
                # Format timestamp
                formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

                prob_value = parse_percentage(probability)/100
                
                # Determine probability class for color coding
                prob_class = "probability-high" if prob_value > 70 else \
                           "probability-medium" if prob_value > 40 else \
                           "probability-low"
                
                
                # Display results with formatting
                st.markdown(f'<div class="result-item">Vehicle Number: {veh_num}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-item">Vehicle Passed by on Timestamp: {formatted_timestamp}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-item">Accident Probability: <span class="{prob_class}">{prob_value:.2%}</span></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-item">Accident Severity: {severity}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="result-item">AI Analysis: {output}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.warning("No prediction results found for the given vehicle number.")
        except Exception as e:
            st.error(f"Error submitting data: {str(e)}")
st.markdown('</div>', unsafe_allow_html=True)