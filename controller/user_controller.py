from fastapi import HTTPException
from typing import Optional

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController
from core.security import verify_password


class UserController(BaseController[models.Users, schemas.UserCreate, schemas.UserUpdate]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[models.Users]:
        return db.query(models.Users).filter(models.Users.email == email).first()

    @staticmethod
    def get_by_username(db: Session, *, email: str) -> Optional[models.Users]:

        aa = db.query(models.Users)
        bb = aa.filter_by(email=email)
        return bb.first()

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[models.Users]:
        auth_user = self.get_by_username(db, email=email)
        if not auth_user:
            return None
        if not verify_password(password, auth_user.password):
            return None
        return auth_user

    @staticmethod
    def is_active(cur_user: models.Users) -> bool:
        if cur_user is None:
            raise HTTPException(
                status_code=400,
                detail="Geçersiz token"
            )
        return cur_user.status

    @staticmethod
    def is_superuser(cur_user: models.Users) -> bool:
        return cur_user.roles.name == 'admin'

    @staticmethod
    def is_referee(cur_user: models.Users) -> bool:
        return cur_user.roles.name == 'referee'

    @staticmethod
    def is_user(cur_user: models.Users) -> bool:
        return cur_user.roles.name == 'user'


user = UserController(models.Users)
