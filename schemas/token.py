from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    api_token: str
    # token_type: str


class TokenPayload(BaseModel):
    user_uuid: Optional[UUID] = None
    username: Optional[str] = None
    email: Optional[str] = None


class TokenMessage(BaseModel):
    msg: str
    hash: str

