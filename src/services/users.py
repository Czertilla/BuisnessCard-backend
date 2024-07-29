from logging import getLogger
from typing import override
from schemas.auth import UserUpdate
from utils.absract.service import BaseService
from loguru import logger

# logger = getLogger(__name__)


class UserService(BaseService):
    async def check_username(self, value: str | UserUpdate) -> bool:
        logger.trace(f"checking username: {value=}")
        async with self.uow:
            if isinstance(value, str):
                logger.debug(f"{value=} is username")
                return await self.uow.users.check_username(value)
            elif isinstance(value, UserUpdate):
                logger.debug(f"{value=} is user")
                if await self.uow.users.check_username(value.username):
                    return value.username != getattr(
                        (await self.uow.users.get_by_email(value.email)),
                        "username",
                        None
                    )
            else:
                logger.warning(
                    f"value is not valid instance: {value.__class__}")
