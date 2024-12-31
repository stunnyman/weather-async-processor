
docker run --name redis -p 6379:6379 -d redis:6-alpine

celery -A wap.tasks.app worker --loglevel=info

uvicorn wap.main:app
