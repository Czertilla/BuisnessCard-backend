from typing import override
import uuid

from fastapi_users import schemas


class CreateUpdateDictModel(schemas.CreateUpdateDictModel):
    @override
    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={
                "id",
                "email",
                "is_superuser",
                "is_active",
                "is_verified",
                "oauth_accounts",
            },
        )

    @override
    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={"id"})


class UserRead(schemas.BaseUser[uuid.UUID]):
    username: str

    class Config:
        from_atributes = True


class UserCreate(schemas.BaseUserCreate, CreateUpdateDictModel):
    username: str


class UserUpdate(schemas.BaseUserUpdate, CreateUpdateDictModel):
    username: str
