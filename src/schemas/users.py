
from typing import Annotated
from pydantic import BaseModel, Field


class SSomeResponse(BaseModel):
    username: Annotated[str, Field(max_length=50)]

    class Config:
        from_atributes = True
