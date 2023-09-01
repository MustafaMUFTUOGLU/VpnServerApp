from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# Shared properties
class OtpBase(BaseModel):
    uuid: Optional[UUID]
    status: bool = False
    create_time: Optional[date]

    class Config:
        orm_mode = True


class Otp(OtpBase):
    email: EmailStr
    corporation: str
    img: Optional[str]
    recaptcha: str
    otp: Optional[str]
