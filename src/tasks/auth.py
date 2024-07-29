# from tasks import celery
from fastapi.responses import JSONResponse
from loguru import logger
from pydantic import EmailStr
from fastapi_cache.decorator import cache

from utils.emails import send_email
from utils.enums.url import S3EndPointUrl
from utils.s3_client import S3Client
from utils.settings import Settings

settings = Settings()

s3 = S3Client(
    settings.S3_ACCESS_KEY,
    settings.S3_SECRET_KEY,
    endpoint_url=S3EndPointUrl(S3EndPointUrl.selectel).value,
    bucket_name="BuisnessCard-res"
)


@cache(expire=60)
async def get_verify_body() -> str:
    logger.debug("cache expired, request to s3")
    body = await s3.get_file("verify_message.html")
    logger.success("html file has been got successfuly")
    return body.decode()

# TODO integrate celery for async tasks
# @celery.task
async def send_verify_email(email: EmailStr, token: str) -> None:
    logger.debug("try to get html file and parse")
    html = (await get_verify_body()).replace("{token}", token)
    await send_email(
        recipients=[email],
        subject="Thanks for using TASKraken",
        body=html,
    )
    return JSONResponse(status_code=200, content={"message": "email has been sent"})