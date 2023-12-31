from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController


class UserRoleController(BaseController[models.UsersRoles, schemas.UserCreate, schemas.UserUpdate]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def get_referee(db: Session, *, offset, limit) -> Optional[models.UsersRoles]:
        return db.query(models.UsersRoles).join(models.Roles).filter(models.Roles.name == 'referee').offset(
            offset * limit).limit(limit).all()


user_role = UserRoleController(models.UsersRoles)
