from fastapi import HTTPException
from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController, ModelType
from typing import Any, List
from core.security import verify_password
from schemas import DeviceUserBase


class DeviceUsersController(BaseController[models.DevicesUsers, schemas.DeviceUserBase, schemas.DeviceAddUser]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def add_device_users(db: Session, *, current_user: models.Users, device_uuid: str,
                         users: schemas.DeviceAddUser) -> Any:
        insert_data = []

        try:
            for user_uuid in users.users_uuid:
                kk = {"device_uuid": device_uuid, "user_uuid": user_uuid}
                insert_data.append(DeviceUserBase(
                    device_uuid=device_uuid,
                    user_uuid=user_uuid
                ))

            print(insert_data)
            device_users.create_bulk(db, obj_in=insert_data)

        except Exception as e:
            return False
        finally:
            return True


    @staticmethod
    def delete_device_users(db: Session, *, current_user: models.Users, device_uuid: str,
                         user_uuid: str) -> Any:

        db.query(models.DevicesUsers).filter(models.DevicesUsers.device_uuid == device_uuid,
                                             models.DevicesUsers.user_uuid == user_uuid).delete()
        db.commit()
        return True



device_users = DeviceUsersController(models.DevicesUsers)
