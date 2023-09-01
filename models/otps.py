# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from db.base_class import Base


class Otps(Base):
    __tablename__ = 'otps'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    corporation = Column(String, nullable=False)
    email = Column(String, nullable=False)
    otp = Column(String, nullable=True)
    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
