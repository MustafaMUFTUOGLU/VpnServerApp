from typing import Optional
from sqlalchemy.orm import Session
import models
import schemas
from controller.base import BaseController


class OtpController(BaseController[models.Otps, schemas.Otp, schemas.Otp]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def get_by_email(db: Session, *, email: str) -> Optional[models.Otps]:
        return db.query(models.Otps).filter(models.Otps.email == email).first()

    @staticmethod
    def check_otp(db: Session, *, email: str, otp: str) -> Optional[models.Otps]:
        return db.query(models.Otps).filter_by(email=email, otp=otp, status=False).first()

    @staticmethod
    def check_user_group(db: Session, *, group_id: str, current_user: models.Otps) -> Optional[models.Otps]:
        return db.query(models.Otps).filter(models.Otps.uuid == group_id,
                                              models.Otps.create_user == current_user.uuid).first()


otp = OtpController(models.Otps)
