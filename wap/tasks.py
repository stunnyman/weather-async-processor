from celery import Celery
from wap.models.weather_service import WeatherService
from wap.models.city import City
from wap.utils.utils import filter_temperature, CURRENT_API_URL, CURRENT_API_KEY, CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import os
import json


app = Celery('weather_tasks', broker=CELERY_BROKER_URL)
weather_service = WeatherService(
    api_url=CURRENT_API_URL,
    api_key=CURRENT_API_KEY
)
app.conf.result_backend = CELERY_RESULT_BACKEND

@app.task(bind=True)
def process_weather_data(self, cities: list):
    results = {}
    for city_i in cities:
        city = City(name=city_i)
        city.normalize_name()
        city.search_city()
        city_data = weather_service.fetch_current_weather(city)
        if not city_data or filter_temperature(city_data):
            continue
        city.set_region(city_data)
        if city.region not in results.keys():
            results[city.region] = []

        results[city.region].append({
            "city": city.name,
            "temperature": city_data.get('temperature'),
            "description": city_data.get('description')
        })

    task_id = self.request.id
    for region, data in results.items():
        region_folder = f"weather_data/{region}"
        os.makedirs(region_folder, exist_ok=True)
        filename = f"{region_folder}/task_{task_id}.json"
        with open(filename, "w") as f:
            json.dump(data, f)
    return {
        "task_id": task_id,
        "status": "completed",
        "results": results
    }
