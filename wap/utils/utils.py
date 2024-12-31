import re
import os
from fastapi import HTTPException
from wap.utils.logger import logger

WEATHERAPI_URL = os.getenv('WEATHERAPI_URL', 'https://api.weatherapi.com/v1/current.json')
WEATHERAPI_KEY = os.getenv('WEATHERAPI_KEY')
WEATHERBIT_URL = os.getenv('WEATHERBIT_URL', 'https://api.weatherbit.io/v2.0/current')
WEATHERBIT_KEY = os.getenv('WEATHERBIT_KEY')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
MIN_TEMP = -50.0
MAX_TEMP = 50.0


def validate_city_names(cities: list):
    if not cities:
        logger.warning(f"Empty data")
        raise HTTPException(
            status_code=400,
            detail=f"Empty data"
        )

    city_name_pattern = re.compile(r'^[a-zA-Zа-яА-Я\s\-]+$')
    invalid_cities = [city for city in cities if not city_name_pattern.match(city)]
    if invalid_cities:
        logger.warning(f"Invalid city names: {', '.join(invalid_cities)}")
        raise HTTPException(
            status_code=400,
            detail=f"Invalid city names: {', '.join(invalid_cities)}"
        )

def validate_weatherapi_response(data) -> list:
    missing_keys = []

    if not data:
        missing_keys.append('data')
    if "current" not in data:
        missing_keys.append("'current' data")
    else:
        current_data = data["current"]
        if "temp_c" not in current_data:
            missing_keys.append("'temp_c' in 'current' data")
        if not current_data.get("condition", {}).get("text"):
            missing_keys.append("'condition' or 'text' in 'current' data")

    if "location" not in data or "tz_id" not in data.get("location", {}):
        missing_keys.append("'location' or 'tz_id' for timezone")

    return missing_keys

def validate_weatherbit_response(data) -> list:
    missing_keys = []

    if not data or "data" not in data:
        missing_keys.append('data')

    if "temp" not in data["data"]:
        missing_keys.append("'temp' in 'data'")

    if "weather" not in data["data"] or "description" not in data["data"]["weather"]:
        missing_keys.append("'weather:description' in 'data'")

    if "timezone" not in data["data"]:
        missing_keys.append("'timezone' in 'data'")

    return missing_keys

def filter_temperature(city_data):
    temperature = city_data.get('temperature')
    if temperature is None or temperature < MIN_TEMP or temperature > MAX_TEMP:
        return True
    return False
