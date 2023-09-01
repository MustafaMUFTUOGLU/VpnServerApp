import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import controller
import models
import schemas
from api import deps

router = APIRouter()


@router.get("")
def search_emails(
        search: str = None,
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Search emails.
    """
    if search and len(search) > 2:
        return controller.approved_email.search(db, search)
    return []


@router.get("/all")
def get_all_emails(
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    Retrieve all emails.
    """
    return controller.approved_email.get_all(db)


@router.post("", response_model=schemas.ApprovedEmailBase)
def create_domain(
        domain_add: schemas.ApprovedEmailBase,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create emails.
    """
    if controller.approved_email.check_domain(db, domain=domain_add.domain) is None:
        domain_id = str(uuid.uuid4())
        domain_add.uuid = domain_id
        domain = controller.approved_email.create(db, obj_in=domain_add)
        return domain
    raise HTTPException(
        status_code=400, detail="Bu domain daha önce kayıt edilmiştir."
    )


@router.put("", response_model=schemas.ApprovedEmailBase)
def update_domain(
        domain_data: schemas.ApprovedEmailBase,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Update emails.
    """
    db_obj = controller.approved_email.get_uuid(db, domain_data.uuid)
    if db_obj:
        domain_update = jsonable_encoder(domain_data)
        domain = controller.approved_email.update(db, db_obj=db_obj, obj_in=domain_update)
        return domain
    raise HTTPException(
        status_code=400, detail="Böyle  bir domain bulunamamıştır."
    )


@router.delete("/{domain_id}")
def delete_domain(
        domain_id: str,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Delete emails.
    """
    # controller.approved_email.delete(db, id=domain_id)
    return {'success': True}
