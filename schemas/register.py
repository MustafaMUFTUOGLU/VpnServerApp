from typing import Dict, Optional
from pydantic import BaseModel
import schemas


class Register(BaseModel):
    user: schemas.UserRegister
    group: Optional[list[schemas.Group]]
    group_name: Optional[str]
    hash: str

    class Config:
        orm_mode = True
