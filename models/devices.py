# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from db.base_class import Base


class Device(Base):
    __tablename__ = 'device'

    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    user_uuid = Column(ForeignKey('users.uuid'), nullable=False)
    ProxyHostName = Column(String, nullable=True)
    ProxyPort = Column(Integer, nullable=False)
    ProxyType = Column(Integer, nullable=False)
    ServerConfiguration_HashedPassword = Column(String, nullable=False)
    UserList_AuthPassword = Column(String, nullable=False)
    UserList_AuthNtLmSecureHash = Column(String, nullable=False)
    VPN_HashedPassword = Column(String, nullable=False)
    VPN_SecurePassword = Column(String, nullable=False)
    ServerHostName = Column(String, nullable=True)
    AccountName = Column(String, nullable=True)
    HubName = Column(String, nullable=True)
    AccountUserName = Column(String, nullable=True)
    AccountPasswordHash = Column(String, nullable=True)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    users = relationship('User', secondary='device_user', back_populates='devices')
