# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class Roles(Base):
    __tablename__ = 'roles'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_user = Column(UUID, nullable=False)
    last_update_user = Column(UUID, nullable=False)

    users = relationship('Users', back_populates='roles')
    # users = relationship('Users', secondary='users_roles', back_populates='roles')
