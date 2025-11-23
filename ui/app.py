"""
Tourism AI Agent - Streamlit Interface
Main application file
"""

import streamlit as st
import sys
from pathlib import Path

# Add project root to path (parent of ui folder)
root_path = Path(__file__).parent.parent
sys.path.insert(0, str(root_path))

from agents.parent_agent import TourismAgent
from agents.weather_agent import WeatherAgent
from utils.api_helpers import format_temperature, format_percentage

# Page configuration
st.set_page_config(
    page_title="Tourism AI Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .weather-card {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
    }
    .places-card {
        background-color: #f0fff0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2ecc71;
        margin-bottom: 1rem;
    }
    .attraction-item {
        padding: 1rem;
        margin: 0.5rem 0;
        background-color: white;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
    }
    .error-card {
        background-color: #fff5f5;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #e74c3c;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'agent' not in st.session_state:
    st.session_state.agent = TourismAgent()

# Header
st.markdown('<div class="main-header">✈️ Tourism AI Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your intelligent travel companion for weather and attractions</div>', unsafe_allow_html=True)

# Main input
st.markdown("### 🗨️ What would you like to know?")
user_input = st.text_input(
    "",
    placeholder="e.g., I'm going to Bangalore, let's plan my trip",
    label_visibility="collapsed"
)

# Example queries
with st.expander("💡 See example queries"):
    st.markdown("""
    - "I'm going to Paris, let's plan my trip"
    - "What's the weather in Tokyo?"
    - "I'm visiting London, what are the places I can visit?"
    - "Tell me about New York weather and tourist spots"
    """)

# Process query
if user_input and len(user_input.strip()) > 0:
    with st.spinner('🔍 Processing your request...'):
        results = st.session_state.agent.process_query(user_input)
    
    # Display error if any
    if not results['success']:
        st.markdown('<div class="error-card">', unsafe_allow_html=True)
        st.error(f"❌ {results['error']}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Display location
        st.success(f"📍 Location: **{results['location']}**")
        
        # Create columns for weather and places
        col1, col2 = st.columns([1, 1])
        
        # Display weather information
        if results['weather']:
            with col1:
                st.markdown('<div class="weather-card">', unsafe_allow_html=True)
                st.markdown("### 🌤️ Weather Information")
                
                weather = results['weather']
                current = weather['current']
                forecast = weather['forecast']
                
                # Current weather
                st.markdown("#### Current Conditions")
                
                col_temp, col_humid = st.columns(2)
                with col_temp:
                    st.metric(
                        "Temperature",
                        format_temperature(current['temperature']),
                        delta=None
                    )
                with col_humid:
                    st.metric(
                        "Humidity",
                        format_percentage(current['humidity']),
                        delta=None
                    )
                
                # Weather description
                weather_desc = WeatherAgent.get_weather_description(current['weather_code'])
                st.info(f"☁️ {weather_desc}")
                
                # Precipitation
                if current['precipitation'] > 0:
                    st.warning(f"🌧️ Current precipitation: {current['precipitation']} mm")
                
                # 3-day forecast
                st.markdown("#### 3-Day Forecast")
                
                for i in range(min(3, len(forecast['dates']))):
                    date = forecast['dates'][i]
                    max_temp = forecast['max_temps'][i]
                    min_temp = forecast['min_temps'][i]
                    rain_prob = forecast['precipitation_probability'][i]
                    
                    with st.container():
                        forecast_col1, forecast_col2, forecast_col3 = st.columns(3)
                        
                        with forecast_col1:
                            st.text(f"📅 {date}")
                        with forecast_col2:
                            st.text(f"🌡️ {format_temperature(min_temp)} - {format_temperature(max_temp)}")
                        with forecast_col3:
                            st.text(f"💧 Rain: {format_percentage(rain_prob)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # Display places information
        if results['places']:
            with col2 if results['weather'] else st.container():
                st.markdown('<div class="places-card">', unsafe_allow_html=True)
                st.markdown("### 🏛️ Tourist Attractions")
                
                places = results['places']
                attractions = places['attractions']
                
                if not attractions:
                    st.info(places.get('message', 'No attractions found'))
                else:
                    st.markdown(f"Found **{len(attractions)}** attractions nearby:")
                    
                    for idx, attraction in enumerate(attractions, 1):
                        st.markdown('<div class="attraction-item">', unsafe_allow_html=True)
                        
                        # Attraction name and type
                        st.markdown(f"**{idx}. {attraction['name']}**")
                        st.caption(f"📍 Type: {attraction['type'].replace('_', ' ').title()}")
                        
                        # Address if available
                        if attraction['address']:
                            st.text(f"📮 {attraction['address']}")
                        
                        # Description if available
                        if attraction['description']:
                            st.text(f"ℹ️ {attraction['description']}")
                        
                        # Website if available
                        if attraction['website']:
                            st.markdown(f"🔗 [Visit Website]({attraction['website']})")
                        
                        # Map link
                        map_url = f"https://www.openstreetmap.org/?mlat={attraction['latitude']}&mlon={attraction['longitude']}&zoom=15"
                        st.markdown(f"🗺️ [View on Map]({map_url})")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>Powered by Open-Meteo API, OpenStreetMap & Overpass API</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)