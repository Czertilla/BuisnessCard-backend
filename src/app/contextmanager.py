from redis import asyncio as aioredis
from fastapi.concurrency import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi import FastAPI
import sys

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append("..")
import logs.config
import utils.settings
settings = utils.settings.getSettings()

async def startup():
    logs.config.setup()
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


async def shutdown():
    ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await startup()
    yield
    await shutdown()
