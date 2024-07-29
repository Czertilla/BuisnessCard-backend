from logging import getLogger
from typing import override
from schemas.auth import UserUpdate
from utils.absract.service import BaseService
from pydantic import validate_call
from loguru import logger

# logger = getLogger(__name__)


class UserService(BaseService):
    @validate_call
    async def check_username(self, value: str | UserUpdate) -> bool:
        logger.trace(f"checking username: {value=}")
        if isinstance(value, str):
            logger.debug(f"{value=} is username")
        elif isinstance(value, UserUpdate):
            logger.debug(f"{value=} is user")
            value: str = value.username
        else:
            logger.warning(
                f"value is not valid instance: {value.__class__}")
        async with self.uow:
            return await self.uow.users.check_username(value)
