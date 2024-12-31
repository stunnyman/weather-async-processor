from wap.models.city import City
from wap.utils.utils import WEATHERAPI_URL,WEATHERBIT_URL, validate_weatherapi_response, validate_weatherbit_response
import requests
from wap.utils.logger import logger


class WeatherService:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def fetch_current_weather(self, city: City):
        url = f"{self.api_url}?q={city.name}&key={self.api_key}"# WEATHERAPI_URL
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as ex:
            logger.error(f"Error fetching weather data for {city.name}: {ex}")
            return None

        try:
            data = response.json()
            missing_keys = []

            if self.api_url == WEATHERAPI_URL:
                missing_keys = validate_weatherapi_response(data)
            elif self.api_url == WEATHERBIT_URL:
                missing_keys = validate_weatherbit_response(data)

            if missing_keys:
                logger.warning(f"Missing keys for {city.name}: {', '.join(missing_keys)}.")
                return None

            if self.api_url == WEATHERAPI_URL:
                return {
                    "temperature": data["current"]["temp_c"],
                    "description": data["current"]["condition"]["text"],
                    "timezone": data["location"]["tz_id"]
                }
            elif self.api_url == WEATHERBIT_URL:
                return {
                    "temperature": data["data"]["temp"],
                    "description": data["data"]["weather"]["description"],
                    "timezone": data["data"]["timezone"]
                }
        except (ValueError, KeyError) as ex:
            logger.error(f"Error parsing weather data for {city.name}: {ex}")
            return None