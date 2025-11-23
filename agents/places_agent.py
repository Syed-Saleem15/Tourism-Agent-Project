"""
Places Agent - Fetches tourist attractions using Nominatim and Overpass APIs
"""

import requests
from typing import Dict, List, Optional
from utils.api_helpers import make_api_request
import time


class PlacesAgent:
    """Agent responsible for fetching tourist attractions"""
    
    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
    def get_coordinates(self, place_name: str) -> Optional[Dict[str, float]]:
        """
        Get coordinates for a place name using Nominatim
        
        Args:
            place_name: Name of the place
            
        Returns:
            Dictionary with lat/lon or None if not found
        """
        params = {
            'q': place_name,
            'format': 'json',
            'limit': 1
        }
        
        headers = {
            'User-Agent': 'TourismAIAgent/1.0'
        }
        
        response = make_api_request(self.NOMINATIM_URL, params, headers)
        
        if not response['success'] or not response['data']:
            return None
        
        data = response['data']
        
        if len(data) > 0:
            return {
                'lat': float(data[0]['lat']),
                'lon': float(data[0]['lon'])
            }
        
        return None
    
    def get_tourist_attractions(self, latitude: float, longitude: float, 
                               radius: int = 5000, limit: int = 5) -> Dict:
        """
        Get tourist attractions near coordinates using Overpass API
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            radius: Search radius in meters (default 5000m = 5km)
            limit: Maximum number of results (default 5)
            
        Returns:
            Dictionary with attractions or error
        """
        # Overpass QL query for tourist attractions
        query = f"""
        [out:json];
        (
          node["tourism"~"attraction|museum|artwork|viewpoint|zoo|theme_park"]
            (around:{radius},{latitude},{longitude});
          way["tourism"~"attraction|museum|artwork|viewpoint|zoo|theme_park"]
            (around:{radius},{latitude},{longitude});
          node["historic"~"monument|memorial|castle|ruins"]
            (around:{radius},{latitude},{longitude});
          way["historic"~"monument|memorial|castle|ruins"]
            (around:{radius},{latitude},{longitude});
          node["amenity"="place_of_worship"]
            (around:{radius},{latitude},{longitude});
          way["amenity"="place_of_worship"]
            (around:{radius},{latitude},{longitude});
        );
        out center {limit};
        """
        
        response = make_api_request(
            self.OVERPASS_URL,
            data={'data': query},
            method='POST'
        )
        
        if not response['success']:
            return {
                'success': False,
                'error': response.get('error', 'Failed to fetch tourist attractions')
            }
        
        data = response['data']
        elements = data.get('elements', [])
        
        if not elements:
            return {
                'success': True,
                'attractions': [],
                'message': 'No tourist attractions found in this area'
            }
        
        # Parse and format attractions
        attractions = []
        for element in elements[:limit * 2]:  # Get more to filter unnamed ones
            tags = element.get('tags', {})
            
            # Skip if no name and no useful description
            name = tags.get('name', '')
            description = tags.get('description', '')
            
            # Skip unnamed attractions unless they have a description
            if not name and not description:
                continue
            
            # Get coordinates (for ways, use center)
            if 'center' in element:
                lat = element['center']['lat']
                lon = element['center']['lon']
            else:
                lat = element.get('lat')
                lon = element.get('lon')
            
            # Create a better name if unnamed
            if not name:
                attraction_type = tags.get('tourism') or tags.get('historic') or tags.get('amenity', 'attraction')
                name = f"{attraction_type.replace('_', ' ').title()}"
            
            attraction = {
                'name': name,
                'type': tags.get('tourism') or tags.get('historic') or tags.get('amenity', 'attraction'),
                'latitude': lat,
                'longitude': lon,
                'address': tags.get('addr:full') or tags.get('addr:street', ''),
                'website': tags.get('website', ''),
                'description': description
            }
            
            attractions.append(attraction)
            
            # Stop once we have enough named attractions
            if len(attractions) >= limit:
                break
        
        return {
            'success': True,
            'attractions': attractions,
            'count': len(attractions)
        }