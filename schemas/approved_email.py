from typing import Optional
from uuid import UUID

from pydantic import BaseModel


# Shared properties
class ApprovedEmailBase(BaseModel):
    uuid: Optional[UUID]
    domain: str
    corporation: str
    status: bool = True

    class Config:
        orm_mode = True
