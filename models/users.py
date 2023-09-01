# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class Users(Base):
    __tablename__ = 'users'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    person_national_id = Column(String(11), nullable=False)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birth_date = Column(Date)
    email = Column(String, nullable=False)
    mobile_phone = Column(String, nullable=False)
    corporation = Column(String, nullable=False)
    education_level = Column(String, nullable=False)
    address = Column(String, nullable=False)
    password = Column(String, nullable=False)

    failed_password_attempt_count = Column(Integer)
    last_login_time = Column(DateTime)
    login_count_failed = Column(Integer)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_user = Column(UUID)
    last_update_user = Column(UUID)

    users_roles = relationship('UsersRoles', back_populates='users')
    group = relationship('Groups', primaryjoin='Users.uuid == Groups.create_user')
