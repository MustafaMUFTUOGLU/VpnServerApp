from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class UserRoles(BaseModel):
    role_uuid: UUID
    user_uuid: UUID
    last_update_user: Optional[UUID]
    create_user: Optional[UUID]

    class Config:
        orm_mode = True
