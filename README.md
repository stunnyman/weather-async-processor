
docker run --name redis -p 6379:6379 -d redis:6-alpine
celery -A wap.tasks.app worker --loglevel=info
uvicorn wap.main:app


**ENV**

By default, the service works with the following API URL:
***api.weatherapi.com*** Also you can change with ENV 'WEATHERAPI_URL'
https://api.weatherapi.com/v1/current.json

However, it also supports working with an alternative API available at:
***weatherbit.io*** Also you can change with ENV 'WEATHERBIT_URL'
https://api.weatherbit.io/v2.0/current

1.You can configure the service to use the alternative API by specifying the desired URL in the configuration settings.

    CURRENT_API_URL
    CURRENT_API_KEY

2.Settings for Celery:

    CELERY_BROKER_URL   
    CELERY_BROKER_URL
    this is default value for both- 'redis://localhost:6379/0'



[
You need to create a system for asynchronous weather data processing that:
1. Accepts a list of cities from the user via an HTTP POST request.
2. Fetches weather data for each city using an external API.
3. Saves the processed results in a specific format for further analysis.
However, you must account for the following complexities:

Requirements:
● Use Celery and Redis for asynchronous processing.
● API errors must be logged with error details.
● Code must be structured to scale for multiple regions.
● Additional implementation requirements:
○ Validate input using regular expressions.
○ Support API keys for multiple external services.
]
