# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, String, text, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID

from db.base_class import Base


class Groups(Base):
    __tablename__ = 'groups'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    person_national_id = Column(String(11), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    corporation = Column(String, nullable=False)
    birth_date = Column(Date)
    education_level = Column(String, nullable=False)
    profession = Column(String, nullable=False)
    mobile_phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    group_name = Column(String, nullable=False)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_user = Column(ForeignKey('users.uuid'), nullable=False)
    last_update_user = Column(UUID, nullable=False)
