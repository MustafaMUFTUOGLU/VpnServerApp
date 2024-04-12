# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text, Table
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from db.base_class import Base


class DevicesUsers(Base):
    __tablename__ = 'devices_users'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    user_uuid = Column(ForeignKey('users.uuid'), nullable=False)
    device_uuid = Column(ForeignKey('devices.uuid'), nullable=False)

# class DeviceUser(Base):
#     __tablename__ = 'device_user'
#
#     user_uuid = Column( ForeignKey('user.uuid'), nullable=False),
#     device_uuid = Column(  ForeignKey('device.uuid'), nullable=False)
#
