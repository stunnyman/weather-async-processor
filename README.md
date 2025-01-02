
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