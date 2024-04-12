# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text, Table
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from db.base_class import Base


user_group_association = Table('user_group_association', Base.metadata,
    Column('user_uuid', Integer, ForeignKey('user.uuid')),
    Column('device_uuid', Integer, ForeignKey('device.uuid'))
)


# class DeviceUser(Base):
#     __tablename__ = 'device_user'
#
#     user_uuid = Column( ForeignKey('user.uuid'), nullable=False),
#     device_uuid = Column(  ForeignKey('device.uuid'), nullable=False)
#

