from datetime import date, datetime
from typing import Optional, Union, List
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, validator

import schemas


# Shared properties

class DeviceUserBase(BaseModel):
    device_uuid: UUID
    user_uuid: UUID

    class Config:
        orm_mode = True



class DeviceAddUser(BaseModel):
    users_uuid: List[UUID]


class DeviceAddUserResponse(BaseModel):
    data: str
