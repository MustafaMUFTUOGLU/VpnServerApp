from typing import Generator

from core import security
from core.config import settings
from db.database import SessionLocal
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
import controller
import models
import schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/oauth"
)


def controlUser (db, token):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kimlik bilgileri doğrulanamadı",
        )

    usr = controller.user.get(db, id=str(token_data.user_uuid))
    if not controller.user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return usr


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.Users:
    return controlUser(db, token)


def get_current_active_user(
        current_user: models.Users = Depends(get_current_user),
) -> models.Users:
    if not controller.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Kullanıcı aktif değil")
    return current_user


def get_current_active_referee(
        current_user: models.Users = Depends(get_current_user),
) -> models.Users:
    if not controller.user.is_referee(current_user):
        raise HTTPException(status_code=400, detail="Kullanıcınızın yetkisi bulunmamaktadır")
    return current_user


def get_current_active_referee_or_admin(
        current_user: models.Users = Depends(get_current_user),
) -> models.Users:
    if not controller.user.is_referee(current_user) and not controller.user.is_superuser(current_user):
        raise HTTPException(status_code=400, detail="Kullanıcınızın yetkisi bulunmamaktadır")
    return current_user


def get_current_active_superuser(
        current_user: models.Users = Depends(get_current_user),
) -> models.Users:
    if not controller.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="Kullanıcınızın yetkisi bulunmamaktadır"
        )
    return current_user
