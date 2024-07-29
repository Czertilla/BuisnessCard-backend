from celery import Celery
from utils.settings import getSettings

settings = getSettings()

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    broker_connection_retry_on_startup=True
)
