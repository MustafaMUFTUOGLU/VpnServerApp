from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController


class RoleController(BaseController[models.Roles, schemas.UserCreate, schemas.UserUpdate]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def find_by_name(db: Session, *, name: str) -> Optional[models.Roles]:
        return db.query(models.Roles).filter(
            models.Roles.name == name).first()


role = RoleController(models.Roles)
