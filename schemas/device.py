from datetime import date, datetime
from typing import Optional, Union, List
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, validator

import schemas


# Shared properties
class DeviceBase(BaseModel):
    uuid: Optional[UUID]
    device_uuid: Optional[UUID]
    create_time: Optional[date]
    last_update_time: Optional[date]
    status: bool = True
    users: List[schemas.UserList]
    Name: str

    class Config:
        orm_mode = True


class DeviceList(BaseModel):
    uuid: Optional[UUID]
    status: bool
    WanIp: str
    Name: str

    class Config:
        orm_mode = True


class DeviceResponse(BaseModel):
    data: DeviceBase


class DeviceListResponse(BaseModel):
    data: List[DeviceList]


class Device(DeviceBase):
    vpnazure: str
    username: str
    password: str


# Properties to receive via API on creation
class DeviceCreate(DeviceBase):
    vpnazure: str
    username: str
    password: str





# Properties to receive via API on update

class DeviceNameUpdate(BaseModel):
    Name: str


class DeviceUpdate(DeviceBase):
    vpnazure: str
    username: str
    password: str


class DeviceDelete(BaseModel):
    duid: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class DeviceCommand(BaseModel):
    ipaddr: str
    status: bool
