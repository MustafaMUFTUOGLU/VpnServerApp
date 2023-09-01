from typing import Optional, List

from sqlalchemy.orm import Session

import models
import schemas
from controller.base import BaseController
from models import ApprovedEmails


class ApprovedEmailController(
    BaseController[models.ApprovedEmails, schemas.ApprovedEmailBase, schemas.ApprovedEmailBase]):

    def __init__(self, model):
        super().__init__(model)

    @staticmethod
    def check_domain(db: Session, *, domain: str) -> Optional[models.ApprovedEmails]:
        return db.query(models.ApprovedEmails).filter_by(domain=domain).first()

    @staticmethod
    def check_email(db: Session, *, email_domain: str, corporation: str) -> Optional[models.ApprovedEmails]:
        return db.query(models.ApprovedEmails).filter(models.ApprovedEmails.domain == email_domain,
                                                      models.ApprovedEmails.corporation == corporation,
                                                      models.ApprovedEmails.status == True).first()

    @staticmethod
    def search(db: Session, search: str) -> list[ApprovedEmails]:
        return db.query(models.ApprovedEmails).filter(models.ApprovedEmails.corporation.ilike(f"%{search}%")).all()


approved_email = ApprovedEmailController(models.ApprovedEmails)
