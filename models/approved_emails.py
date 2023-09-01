# coding: utf-8
from sqlalchemy import Boolean, Column, String, text
from sqlalchemy.dialects.postgresql.base import UUID

from db.base_class import Base


class ApprovedEmails(Base):
    __tablename__ = 'approved_emails'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    corporation = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    status = Column(Boolean, nullable=False, server_default=text("true"))
