"""Module météo utilisant OpenWeatherMap API.

Fonctionnalités:
- Température actuelle
- Conditions météo
- Ville configurable
"""
import requests
from typing import Dict, Any, Optional


class WeatherService:
    def __init__(self, api_key: str, city: str = "Lyon"):
        self.api_key = api_key
        self.city = city
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self) -> Optional[Dict[str, Any]]:
        """Récupère la météo actuelle."""
        if not self.api_key:
            return {
                'error': 'API key non configurée',
                'message': 'Ajoutez votre clé API OpenWeatherMap dans data/config.json'
            }

        try:
            params = {
                'q': self.city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'fr'
            }
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'city': data['name'],
                    'temperature': round(data['main']['temp'], 1),
                    'feels_like': round(data['main']['feels_like'], 1),
                    'description': data['weather'][0]['description'].capitalize(),
                    'humidity': data['main']['humidity'],
                    'icon': data['weather'][0]['icon']
                }
            elif response.status_code == 401:
                return {'error': 'Clé API invalide'}
            else:
                return {'error': f'Erreur {response.status_code}'}
        except requests.RequestException as e:
            return {'error': f'Erreur réseau: {str(e)}'}
