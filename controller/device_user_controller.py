from fastapi import HTTPException
from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController, ModelType
from core.security import verify_password


class DeviceController(BaseController[models.Devices, schemas.DeviceCreate, schemas.DeviceUpdate]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def get_devices(db: Session, *, current_user: models.Users) -> list[tuple[ModelType]]:
        return db.query(models.Devices).join(models.DevicesUsers).filter(
            models.DevicesUsers.user_uuid == current_user.uuid).all()

    @staticmethod
    def sendmessage_devices(db: Session, *, current_user: models.Users) -> Optional[schemas.DeviceCommand]:
        return db.query(models.Devices).all()

    @staticmethod
    def get_device_by_id(db: Session, *, current_user: models.Users, device_uuid: str) -> Optional[
        schemas.DeviceBase]:
        return (db.query(models.Devices)
                .join(models.DevicesUsers)
                .join(models.Users)
                .filter(models.DevicesUsers.user_uuid == current_user.uuid,
                        models.DevicesUsers.device_uuid == device_uuid)
                .join(models.Roles)
                .first())


device = DeviceController(models.Devices)
