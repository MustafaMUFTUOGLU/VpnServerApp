from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, validator


# Shared properties
class GroupBase(BaseModel):
    uuid: Optional[UUID]
    last_update_user: Optional[UUID]
    create_user: Optional[UUID]
    create_time: Optional[date]
    last_update_time: Optional[date]
    status: bool = True

    birth_date: date
    @validator("birth_date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()

    class Config:
        orm_mode = True


class Group(GroupBase):
    group_name: Optional[str]
    person_national_id: str = Field(None, max_length=11, min_legnth=11)
    name: str
    surname: str
    email: EmailStr
    mobile_phone: str = Field(None, max_length=11, min_legnth=10)
    education_level: str
    profession: str
    corporation: str


class GroupDelete(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True
