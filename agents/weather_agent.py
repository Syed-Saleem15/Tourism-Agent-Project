"""
Weather Agent - Fetches weather data from Open-Meteo API
"""

import requests
from typing import Dict, Optional
from utils.api_helpers import make_api_request


class WeatherAgent:
    """Agent responsible for fetching weather information"""
    
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather(self, latitude: float, longitude: float) -> Dict:
        """
        Get current weather and forecast for a location
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            Dictionary with weather data or error
        """
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max',
            'timezone': 'auto',
            'forecast_days': 3
        }
        
        response = make_api_request(self.BASE_URL, params)
        
        if not response['success']:
            return {
                'success': False,
                'error': response.get('error', 'Failed to fetch weather data')
            }
        
        data = response['data']
        
        # Parse current weather
        current = data.get('current', {})
        daily = data.get('daily', {})
        
        return {
            'success': True,
            'current': {
                'temperature': current.get('temperature_2m'),
                'humidity': current.get('relative_humidity_2m'),
                'precipitation': current.get('precipitation'),
                'weather_code': current.get('weather_code')
            },
            'forecast': {
                'max_temps': daily.get('temperature_2m_max', []),
                'min_temps': daily.get('temperature_2m_min', []),
                'precipitation_probability': daily.get('precipitation_probability_max', []),
                'dates': daily.get('time', [])
            },
            'timezone': data.get('timezone', 'UTC')
        }
    
    @staticmethod
    def get_weather_description(weather_code: int) -> str:
        """
        Convert weather code to human-readable description
        
        Args:
            weather_code: WMO weather code
            
        Returns:
            Weather description string
        """
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Foggy",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        return weather_codes.get(weather_code, "Unknown")