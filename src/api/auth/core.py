import uuid
from typing import Optional, override

from fastapi import Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_users import BaseUserManager, UUIDIDMixin, models, exceptions, schemas
from fastapi_users.jwt import generate_jwt, decode_jwt
import jwt

from repositories.users import get_user_db
from models.users import UserORM
from schemas.auth import UserCreate, UserUpdate
from services.users import UserService
from tasks.auth import send_verify_email
from units_of_work.user import UserUOW
from utils.settings import getSettings
from logging import getLogger

SECRET = getSettings().PASSW_SECTRET

logger = getLogger(__name__)


class UserManager(UUIDIDMixin, BaseUserManager[UserORM, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def check_username(self, user: UserCreate|UserUpdate):
        if await UserService(UserUOW()).check_username(user):
            raise HTTPException(
                status_code=409,
                detail={
                    "loc": [
                        "username"
                    ],
                    "msg": "username is already exists",
                    "input": user.username
                }
            )

    @override
    async def create(
            self, 
            user_create: UserCreate, 
            safe: bool = False, 
            request: Request | None = None
    ) -> UserORM:
        await self.check_username(user_create)
        return await super().create(user_create, safe, request)
    
    @override
    async def update(
            self, 
            user_update: UserUpdate, 
            user: UserORM, 
            safe: bool = False, 
            request: Request | None = None
    ) -> UserORM:
        await self.check_username(user_update)
        return await super().update(user_update, user, safe, request)

    @override
    async def on_after_register(self, user: UserORM, request: Optional[Request] = None):
        logger.info(f"User {user.id} has registered.")

    @override
    async def on_after_forgot_password(
        self, user: UserORM, token: str, request: Optional[Request] = None
    ):
        logger.warning(
            f"User {user.id} has forgot their password. Reset token: {token}")

    @override
    async def on_after_request_verify(
        self, user: UserORM, token: str, request: Optional[Request] = None
    ) -> JSONResponse:
        logger.warning(
            f"Verification requested for user {user.id}. Verification token: {token}"
        )
        return await send_verify_email(user.email, token)

    @override
    async def request_verify(
        self, user: models.UP, request: Optional[Request] = None
    ) -> JSONResponse:
        if not user.is_active:
            raise exceptions.UserInactive()
        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        token_data = {
            "sub": str(user.id),
            "email": user.email,
            "aud": self.verification_token_audience,
        }
        token = generate_jwt(
            token_data,
            self.verification_token_secret,
            self.verification_token_lifetime_seconds,
        )
        return await self.on_after_request_verify(user, token, request)

    @override
    async def verify(self, token: str, request: Optional[Request] = None) -> models.UP:
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken()

        try:
            user_id = data["sub"]
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken()

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken()

        try:
            parsed_id = self.parse_id(user_id)
        except exceptions.InvalidID:
            raise exceptions.InvalidVerifyToken()

        if parsed_id != user.id:
            raise exceptions.InvalidVerifyToken()

        if user.is_verified:
            raise exceptions.UserAlreadyVerified()

        verified_user = await self._update(
            user,
            {
                "is_verified": True,
                "role": "specialist"
            }
        )

        await self.on_after_verify(verified_user, request)

        return verified_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
