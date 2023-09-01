# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


class UsersRoles(Base):
    __tablename__ = 'users_roles'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    user_uuid = Column(ForeignKey('users.uuid'), nullable=False)
    role_uuid = Column(ForeignKey('roles.uuid'), nullable=False)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_user = Column(UUID, nullable=False)
    last_update_user = Column(UUID, nullable=False)

    roles = relationship('Roles')
    users = relationship('Users', back_populates='users_roles')
