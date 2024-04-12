import requests
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import Any, List

from starlette.responses import JSONResponse

import controller
import models
import schemas
from api import deps

router = APIRouter()


@router.get("", response_model=schemas.DeviceListResponse)
def get_devices(
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve group info.
    """
    # devicelist = schemas.DeviceList

    # retval = []

    # deviceslist = []
    devices = controller.device.get_devices(db, current_user=current_user)
    # for device in devices:
    #     retval.append({"uuid": device.uuid,
    #                  "status": device.status,
    #                  "WanIp": device.WanIp})
    return {
        "data": devices
    }


@router.get("/{device_uuid}", response_model=schemas.DeviceResponse)
def read_device_by_id(
        device_uuid: str,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    device = controller.device.get_device_by_id(db, current_user=current_user, device_uuid=device_uuid)
    return {
        "data": device
    }

@router.put("/{device_uuid}", response_model=schemas.DeviceResponse)
def read_device_by_id(
        device_uuid: str,
        new_name: schemas.DeviceNameUpdate,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    device = controller.device.get_uuid(db, id=device_uuid)
    device_update = jsonable_encoder(device)
    device_update["Name"] = new_name.Name

    controller.device.update(db, db_obj=device, obj_in=device_update)
    return {
        "data": device
    }


@router.post("/{device_uuid}/user", response_model=schemas.DeviceAddUserResponse)
def device_user_add(
        device_uuid: str,
        users_uuid: schemas.DeviceAddUser,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    return {
        "data": controller.device_users.add_device_users(db, current_user=current_user, device_uuid=device_uuid, users=users_uuid)
    }

@router.delete("/{device_uuid}/user/{user_uuid}", response_model=schemas.DeviceAddUserResponse)
def device_user_delete(
        device_uuid: str,
        user_uuid: str,
        current_user: models.Users = Depends(deps.get_current_active_superuser),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    return {
        "data": controller.device_users.delete_device_users(db, current_user=current_user, device_uuid=device_uuid, user_uuid=user_uuid)
    }
