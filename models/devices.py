# coding: utf-8
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship
from db.base_class import Base


class Devices(Base):
    __tablename__ = 'devices'
    uuid = Column(UUID, primary_key=True, server_default=text("uuid_generate_v4()"))
    Name = Column(String, nullable=True)
    ProxyHostName = Column(String, nullable=True)
    ProxyPort = Column(Integer, nullable=True)
    ProxyType = Column(Integer, nullable=True)
    ServerConfiguration_HashedPassword = Column(String, nullable=True)
    UserList_AuthPassword = Column(String, nullable=True)
    UserList_AuthNtLmSecureHash = Column(String, nullable=True)
    VPN_HashedPassword = Column(String, nullable=True)
    VPN_SecurePassword = Column(String, nullable=True)
    ServerHostName = Column(String, nullable=True)
    AccountName = Column(String, nullable=True)
    HubName = Column(String, nullable=True)
    AccountUserName = Column(String, nullable=True)
    AccountPasswordHash = Column(String, nullable=True)
    WanIp = Column(String, nullable=True)

    status = Column(Boolean, nullable=False, server_default=text("true"))
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    last_update_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    # many to many ilişkilerinde seocondary property'si ile ilişki tablosu belirtilir,
    # back_populates ile de device tablosunda değişiklik olduğunda, device tablosuyla ilişkili olan alanlar güncellenir
    users = relationship('Users', secondary='devices_users', back_populates='devices')
