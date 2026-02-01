"""
Weather and News Skills - Get weather forecasts and news briefings

Provides weather information and news updates.
"""

import requests
from datetime import datetime
from typing import Dict
from skills import BaseSkill


class WeatherNewsSkills(BaseSkill):
    """Weather and news information."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.weather_api_key = config.get('integrations', {}).get('openweather_api_key', '')
        self.news_api_key = config.get('integrations', {}).get('news_api_key', '')
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        info_intents = [
            'get_weather',
            'get_forecast',
            'get_news',
            'get_headlines',
            'weather_today'
        ]
        return intent in info_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute weather/news commands."""
        try:
            if intent in ['get_weather', 'weather_today', 'get_forecast']:
                location = entities.get('location', 'London')  # Default location
                return self._get_weather(location)
            elif intent in ['get_news', 'get_headlines']:
                category = entities.get('category', 'general')
                return self._get_news(category)
            else:
                return "I can provide weather or news information."
        except Exception as e:
            self.logger.error(f"Weather/News error: {e}")
            return f"Error getting information: {str(e)}"
    
    def _get_weather(self, location: str) -> str:
        """Get weather information using OpenWeatherMap API."""
        if not self.weather_api_key:
            return (
                "Weather API not configured. Get a free API key from:\n"
                "https://openweathermap.org/api\n"
                "Add it to config.yaml under integrations.openweather_api_key"
            )
        
        try:
            # Current weather
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': self.weather_api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            description = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            
            result = f"Weather in {location}:\n"
            result += f"Temperature: {temp}°C (feels like {feels_like}°C)\n"
            result += f"Conditions: {description.capitalize()}\n"
            result += f"Humidity: {humidity}%\n"
            result += f"Wind Speed: {wind_speed} m/s"
            
            return result
            
        except requests.RequestException as e:
            self.logger.error(f"Weather API error: {e}")
            return f"Could not fetch weather data for {location}. Check your API key and location."
    
    def _get_news(self, category: str = 'general') -> str:
        """Get news headlines using NewsAPI."""
        if not self.news_api_key:
            return (
                "News API not configured. Get a free API key from:\n"
                "https://newsapi.org\n"
                "Add it to config.yaml under integrations.news_api_key"
            )
        
        try:
            url = "https://newsapi.org/v2/top-headlines"
            params = {
                'apiKey': self.news_api_key,
                'category': category,
                'country': 'us',
                'pageSize': 5
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'ok' or not data.get('articles'):
                return "No news articles found."
            
            result = f"Top {category.capitalize()} News:\n\n"
            for i, article in enumerate(data['articles'][:5], 1):
                title = article['title']
                source = article['source']['name']
                result += f"{i}. {title}\n   Source: {source}\n\n"
            
            return result.strip()
            
        except requests.RequestException as e:
            self.logger.error(f"News API error: {e}")
            return "Could not fetch news. Check your API key and internet connection."
