from uuid import UUID

from sqlalchemy import ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID


class UserORM(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    photo_folder_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("folders.id"))
