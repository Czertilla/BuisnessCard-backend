from typing import Optional
from database import Base
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from utils.mixins.sqlalchemy import TimestampMixin


class FolderORM(Base):
    __tablename__ = "folders"

    head_folder_id: Mapped[UUID] = mapped_column(
        ForeignKey("folders.id", ondelete='CASCADE'), nullable=True)
    # name: Mapped[str|None] = mapped_column(nullable=True)

    head_folder: Mapped["FolderORM"] = relationship(
        back_populates="folders", remote_side="FolderORM.id")

    files: Mapped[list["FileORM"]] = relationship(back_populates="folder")
    folders: Mapped[list["FolderORM"]] = relationship(
        back_populates="head_folder")


class FileORM(Base, TimestampMixin):
    __tablename__ = "files"

    data: Mapped[bytes | None]
    name: Mapped[str | None]
    folder_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("folders.id", ondelete="CASCADE"))

    folder: Mapped[Optional["FolderORM"]] = relationship(
        back_populates="files")
