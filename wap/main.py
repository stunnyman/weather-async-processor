from celery.result import AsyncResult
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wap.tasks import process_weather_data
from wap.utils.utils import validate_city_names, CELERY_TASKS_PATH
from wap.utils.logger import logger


app = FastAPI()

class WeatherRequest(BaseModel):
    cities: list

@app.post("/weather")
async def post_weather_data(request: WeatherRequest):
    cities = request.cities
    validate_city_names(cities)
    task = process_weather_data.apply_async(args=[cities])
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    task = AsyncResult(task_id)

    if task.state == "PENDING":
        return {"status": "running"}

    elif task.state == "FAILURE":
        return {"status": "failed", "message": str(task.info)}

    elif task.state == "SUCCESS":
        return {"status": "completed", "results": task.result}

    return {"status": "unknown"}


@app.get("/results/{region}")
async def get_results_by_region(region: str):
    region_data = []
    region_path = f"{CELERY_TASKS_PATH}/{region}"

    if not os.path.exists(region_path):
        logger.warning(f"Region {region} not found.")
        raise HTTPException(status_code=404, detail=f"Region {region} not found.")

    for filename in os.listdir(region_path):
        if filename.endswith(".json"):
            with open(os.path.join(region_path, filename), 'r') as file:
                region_data.append(file.read())

    return {"region": region, "data": region_data}