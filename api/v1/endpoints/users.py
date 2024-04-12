from datetime import datetime
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, ValidationError

import controller
import models
import schemas
from api import deps
from core.security import get_password_hash
from schemas import UserRoles
from utils import send_new_account_email, generate_password

router = APIRouter()


@router.get("/info", response_model=schemas.GroupBase)
def group_info(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve group info.
    """
    response = schemas.GroupBase()
    groups = controller.group.get_user_group(db, current_user=current_user)
    if len(groups) > 0:
        response.user_type = 'Grup'
        response.groups = [f'{x.name} {x.surname}' for x in groups]
        response.groups.append(f'{current_user.name} {current_user.surname}')
        response.group_name = groups[0].group_name
    else:
        response.user_type = 'Bireysel'
        response.groups = [f'{current_user.name} {current_user.surname}']
    return response


@router.get("", response_model=schemas.UserListResponse)
def read_users(
        db: Session = Depends(deps.get_db),
        page: int = 1,
        items_per_page: int = 1000,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve referee users.
    """
    users = controller.user.get_multi(db, create_user=current_user.uuid, offset=(page - 1), limit=items_per_page)

    # aa = schemas.UserListResponse.model_validate(users)

    # for user in users:
    #     if len(user.group) > 0:
    #         user.user_type = 'Grup'
    #         user.groups = [f'{x.name} {x.surname}' for x in user.group]
    #         user.groups.append(f'{user.name} {user.surname}')
    #         user.group_name = user.group[0].group_name
    #     else:
    #         user.user_type = 'Bireysel'

    return {
        "data": users
    }



@router.get("/referee")
def read_users(
        db: Session = Depends(deps.get_db),
        page: int = 0,
        limit: int = 1000,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve referee users.
    """
    users = controller.user_role.get_referee(db, offset=page, limit=limit)
    return [user.users for user in users]


@router.post("", response_model=schemas.UserBase)
def create_user(
        user_add: schemas.UserCreate,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = controller.user.get_by_email(db, email=user_add.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu mail adresi zaten kullanılıyor!",
        )

    password = generate_password(8)

    user_add.create_user = current_user.uuid
    user_add.last_update_user = current_user.uuid
    user_add.password = get_password_hash(password)
    user_add.create_time = datetime.utcnow()
    user_add.last_update_time = datetime.utcnow()
    user_add.status = True

    # del user_add.role

    # if current_user.roles.name == 'admin':
    #     get_role = controller.role.find_by_name(db, name='admin')
    # else:
    get_role = controller.role.find_by_name(db, name='user')

    user_add.roles_uuid = get_role.uuid
    user = controller.user.create(db, obj_in=user_add)

    # role = get_role.name
    #
    # user_role = UserRoles(
    #     user_uuid=user.uuid,
    #     role_uuid=get_role.uuid,
    #     create_user=current_user.uuid,
    #     last_update_user=current_user.uuid,
    # )
    # controller.user_role.create(
    #     db, obj_in=user_role
    # )

    # send_new_account_email(
    #     email=user_add.email, name=user_add.name, surname=user_add.surname,
    #     role=get_role.name, password=password
    # )

    user_add.uuid = user.uuid
    del user_add.password
    return JSONResponse(content={'data': jsonable_encoder(user_add)})


@router.put("", response_model=schemas.User)
def update_user(
        user_data: schemas.UserUpdate,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update own user.
    """
    user_update = jsonable_encoder(user_data)
    if user_update['password'] is None:
        del user_update['password']
    else:
        user_update['password'] = get_password_hash(user_update['password'])

    user_update['uuid'] = current_user.uuid
    user_update['create_user'] = current_user.uuid
    user_update['last_update_user'] = current_user.uuid
    user_update['create_time'] = datetime.utcnow()
    user_update['last_update_time'] = datetime.utcnow()
    user = controller.user.update(db, db_obj=current_user, obj_in=user_update)
    return user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
        user_id: str,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = controller.user.get_uuid(db, id=user_id)
    return user


@router.patch("/{user_id}")
def deactivate_user(
        user_id: str,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Active or Deactivate a user.
    """
    controller.user.deactivate(db, uuid=user_id)
    return {'success': True}


@router.delete("/{user_id}")
def delete_user(
        user_id: str,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_superuser),
) -> Any:
    """
   Delete a user.
    """
    controller.user.delete(db, uuid=user_id)
    return {'success': True}
