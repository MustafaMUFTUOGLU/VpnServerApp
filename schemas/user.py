from datetime import date, datetime
from typing import Optional, Union, List
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field, validator

password_regex = '((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})'


# Shared properties
class UserBase(BaseModel):
    uuid: Optional[UUID]
    last_update_user: Optional[UUID]
    create_user: Optional[UUID]
    create_time: Optional[date]
    last_update_time: Optional[date]
    status: bool = True

    class Config:
        orm_mode = True


class Username(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class User(UserBase):
    person_national_id: str = Field(None, max_length=11, min_legnth=11)
    name: str
    surname: str
    email: Union[EmailStr, str]
    mobile_phone: str = Field(None, max_length=11, min_legnth=10)
    address: str
    education_level: str
    corporation: str
    failed_password_attempt_count: Optional[int]
    last_login_time: Optional[date]
    login_count_failed: Optional[int]
    user_type: Optional[str]
    groups: Optional[List[str]]
    group_name: Optional[str]


class GroupBase(BaseModel):
    user_type: Optional[str]
    groups: Optional[List[str]]
    group_name: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    person_national_id: str = Field(None, max_length=11, min_legnth=11)
    name: str
    surname: str
    email: EmailStr
    mobile_phone: str = Field(None, max_length=11, min_legnth=10)
    address: str
    education_level: str
    corporation: str
    password: Optional[str]
    role: Optional[str]

    birth_date: date

    @validator("birth_date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()


# Properties to receive via API on creation
class UserRegister(UserBase):
    person_national_id: str = Field(None, max_length=11, min_legnth=11)
    name: str
    surname: str
    email: EmailStr
    mobile_phone: str = Field(None, max_length=11, min_legnth=10)
    address: str
    education_level: str
    corporation: str
    password: str = Field(..., regex=password_regex)

    birth_date: date

    @validator("birth_date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()


# Properties to receive via API on update
class UserUpdate(UserBase):
    person_national_id: str = Field(None, max_length=11, min_legnth=11)
    name: str
    surname: str
    email: EmailStr
    mobile_phone: str = Field(None, max_length=11, min_legnth=10)
    address: str
    education_level: str
    corporation: str
    password: Optional[str] = Field(..., regex=password_regex)

    birth_date: date

    @validator("birth_date", pre=True)
    def parse_birthdate(cls, value):
        return datetime.strptime(
            value,
            "%d-%m-%Y"
        ).date()


class UserDelete(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str
    img: str
    recaptcha: str
