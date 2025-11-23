"""
Tourism AI Agent - Parent Agent
Orchestrates child agents based on user intent
"""

import re
from typing import Dict, List, Optional
from agents.weather_agent import WeatherAgent
from agents.places_agent import PlacesAgent


class TourismAgent:
    """Parent agent that orchestrates weather and places agents"""
    
    def __init__(self):
        self.weather_agent = WeatherAgent()
        self.places_agent = PlacesAgent()
    
    def analyze_intent(self, user_input: str) -> Dict[str, bool]:
        """
        Analyze user input to determine what information they want
        
        Args:
            user_input: User's query
            
        Returns:
            Dictionary with boolean flags for weather and places
        """
        user_input_lower = user_input.lower()
        
        # Keywords for weather intent
        weather_keywords = [
            'weather', 'temperature', 'rain', 'forecast', 
            'hot', 'cold', 'climate', 'temp'
        ]
        
        # Keywords for places intent
        places_keywords = [
            'visit', 'places', 'attractions', 'see', 'tour',
            'tourist', 'sights', 'destination', 'spots', 'things to do'
        ]
        
        wants_weather = any(keyword in user_input_lower for keyword in weather_keywords)
        wants_places = any(keyword in user_input_lower for keyword in places_keywords)
        
        # If no specific keywords, assume they want places (trip planning)
        if not wants_weather and not wants_places:
            wants_places = True
        
        return {
            'weather': wants_weather,
            'places': wants_places
        }
    
    def extract_location(self, user_input: str) -> Optional[str]:
        """
        Extract location from user input
        
        Args:
            user_input: User's query
            
        Returns:
            Extracted location or None
        """
        # Skip very short inputs
        if len(user_input.strip()) < 5:
            return None
            
        # Common patterns: "going to X", "visit X", "in X", "to X"
        patterns = [
            r'(?:going to|visit|trip to|travel to)\s+([A-Z][a-zA-Z\s]+?)(?:\,|\.|$|\s+let|\s+what|\s+and)',
            r'(?:in|at)\s+([A-Z][a-zA-Z\s]+?)(?:\,|\.|$|\s+let|\s+what|\s+and)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                location = match.group(1).strip()
                # Skip if location is too short (likely not a real place)
                if len(location) > 2:
                    return location
        
        # If no pattern matches, look for capitalized words (likely place names)
        words = user_input.split()
        for i, word in enumerate(words):
            if word[0].isupper() and word.lower() not in ['i', 'i\'m', 'let\'s', 'what', 'is', 'the', 'and']:
                # Get potentially multi-word location
                location_parts = [word]
                for j in range(i + 1, len(words)):
                    if words[j][0].isupper():
                        location_parts.append(words[j])
                    else:
                        break
                location = ' '.join(location_parts)
                # Only return if it's a substantial location name
                if len(location) > 2:
                    return location
        
        return None
    
    def process_query(self, user_input: str) -> Dict:
        """
        Process user query and return results from appropriate agents
        
        Args:
            user_input: User's query
            
        Returns:
            Dictionary containing results and any errors
        """
        # Extract location
        location = self.extract_location(user_input)
        
        if not location:
            return {
                'success': False,
                'error': 'Could not identify a location in your query. Please mention a place name.',
                'location': None,
                'weather': None,
                'places': None
            }
        
        # Analyze intent
        intent = self.analyze_intent(user_input)
        
        results = {
            'success': True,
            'location': location,
            'weather': None,
            'places': None,
            'error': None
        }
        
        # Get coordinates first (needed for both agents)
        coords = self.places_agent.get_coordinates(location)
        
        if not coords:
            return {
                'success': False,
                'error': f"I'm sorry, I don't know this place exists: {location}",
                'location': location,
                'weather': None,
                'places': None
            }
        
        # Query weather agent if needed
        if intent['weather']:
            weather_data = self.weather_agent.get_weather(coords['lat'], coords['lon'])
            if weather_data['success']:
                results['weather'] = weather_data
            else:
                results['error'] = weather_data.get('error', 'Failed to fetch weather data')
        
        # Query places agent if needed
        if intent['places']:
            places_data = self.places_agent.get_tourist_attractions(coords['lat'], coords['lon'])
            if places_data['success']:
                results['places'] = places_data
            else:
                if results['error']:
                    results['error'] += f" Also: {places_data.get('error', 'Failed to fetch places data')}"
                else:
                    results['error'] = places_data.get('error', 'Failed to fetch places data')
        
        return results