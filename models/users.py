# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from db.base_class import Base


# users: "d3d5e133-b484-49c3-bcfd-f8ba5ce2bb38"	"1"	"mustafa"	"muftuoglu"		"mustafa.muftuoglu88@gmail.com"	"05497721477"	"didielektronik"	"xx"	"xx"	"$2b$12$j560Ht22ayrJ4m88d9rhm.rcjzliX0f6PO/N0bNCF8xqfoR39Jkx2"				true	"2023-09-01 12:21:33.178524"	"2023-09-01 12:21:33.178524"
class Users(Base):
    __tablename__ = 'users'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    email = Column(String, nullable=False)
    mobile_phone = Column(String, nullable=False)
    password = Column(String, nullable=False)

    failed_password_attempt_count = Column(Integer)
    last_login_time = Column(DateTime)
    login_count_failed = Column(Integer)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    create_user = Column(UUID)
    last_update_user = Column(UUID)

    roles_uuid = Column(UUID, ForeignKey('roles.uuid'))
    roles = relationship('Roles', back_populates='users')

    # roles = relationship('Roles', secondary='users_roles', back_populates='users')
    # group = relationship('Groups', primaryjoin='Users.uuid == Groups.create_user')

    devices = relationship('Devices', secondary='devices_users', back_populates='users')
