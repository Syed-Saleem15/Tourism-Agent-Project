"""
API Helper Functions
Shared utilities for making API requests
"""

import requests
from typing import Dict, Optional, Any
import time


def make_api_request(url: str, params: Optional[Dict] = None, 
                    headers: Optional[Dict] = None, 
                    method: str = 'GET',
                    data: Optional[Dict] = None,
                    timeout: int = 10,
                    max_retries: int = 3) -> Dict[str, Any]:
    """
    Make an API request with error handling and retries
    
    Args:
        url: API endpoint URL
        params: Query parameters
        headers: Request headers
        method: HTTP method (GET or POST)
        data: Request body data
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        
    Returns:
        Dictionary with success flag and data or error message
    """
    if headers is None:
        headers = {}
    
    # Add default user agent if not provided
    if 'User-Agent' not in headers:
        headers['User-Agent'] = 'TourismAIAgent/1.0'
    
    for attempt in range(max_retries):
        try:
            if method.upper() == 'GET':
                response = requests.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=timeout
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    params=params,
                    data=data,
                    headers=headers,
                    timeout=timeout
                )
            else:
                return {
                    'success': False,
                    'error': f'Unsupported HTTP method: {method}'
                }
            
            # Check if request was successful
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                return {
                    'success': True,
                    'data': response.json()
                }
            except ValueError:
                return {
                    'success': True,
                    'data': response.text
                }
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))  # Exponential backoff
                continue
            return {
                'success': False,
                'error': 'Request timed out. Please try again.'
            }
            
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                time.sleep(1 * (attempt + 1))
                continue
            return {
                'success': False,
                'error': 'Could not connect to the server. Please check your internet connection.'
            }
            
        except requests.exceptions.HTTPError as e:
            return {
                'success': False,
                'error': f'HTTP error occurred: {e.response.status_code}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'An unexpected error occurred: {str(e)}'
            }
    
    return {
        'success': False,
        'error': 'Maximum retry attempts reached'
    }


def format_temperature(temp: float, unit: str = 'C') -> str:
    """
    Format temperature value
    
    Args:
        temp: Temperature value
        unit: Temperature unit (C or F)
        
    Returns:
        Formatted temperature string
    """
    return f"{temp:.1f}°{unit}"


def format_percentage(value: float) -> str:
    """
    Format percentage value
    
    Args:
        value: Percentage value
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.0f}%"