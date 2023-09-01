from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController


class GroupController(BaseController[models.Groups, schemas.Group, schemas.Group]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[models.Groups]:
        return db.query(models.Groups).filter(models.Groups.email == email).first()

    @staticmethod
    def get_user_group(db: Session, *, current_user: models.Users) -> Optional[models.Groups]:
        return db.query(models.Groups).filter(models.Groups.create_user == current_user.uuid).all()

    @staticmethod
    def check_user_group(db: Session, *, group_id: str, current_user: models.Users) -> Optional[models.Groups]:
        return db.query(models.Groups).filter(models.Groups.uuid == group_id,
                                              models.Groups.create_user == current_user.uuid).first()


group = GroupController(models.Groups)
