from typing import Annotated
from fastapi import Depends, File, UploadFile
from pydantic import BaseModel


async def upload_file(file: UploadFile = File(...)) -> UploadFile:
    return file


async def upload_folder(files: list[UploadFile] = []) -> list[UploadFile]:
    return [await upload_file(file) for file in files]


class SFolderUpload(BaseModel):
    folder: list[Annotated[UploadFile, File(...)]] = Depends(upload_folder)
