import os
import shutil
import uuid
from datetime import date
from typing import Any

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import controller
import models
from api import deps
from core.config import settings

router = APIRouter()


@router.post("/upload")
def upload_file(
        file: UploadFile = File(...),
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload File.
    """
    if file.content_type not in settings.MIME_TYPES:
        raise HTTPException(
            status_code=415,
            detail="Desteklenmeyen dosya formatı.",
        )

    extention = file.filename.split('.')[-1]
    if extention not in settings.FILE_EXTENTIONS:
        raise HTTPException(
            status_code=415,
            detail="Desteklenmeyen dosya formatı.",
        )

    try:
        path = f"{settings.NFS_PATH}/{str(date.today())}"
        file_name = f"{str(uuid.uuid4())}_{file.filename.replace(' ', '_')}"
        os.makedirs(path, exist_ok=True)
        file_path = f"{path}/{file_name}"
        with open(file_path, 'wb+') as f:
            shutil.copyfileobj(file.file, f)
        return JSONResponse(content={'data': {'name': file_name}})
    except Exception as e:
        print(e)


@router.get("/download/{name}")
def download_file(
        name: str,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_user),
) -> Any:
    """
    Download File.
    """
    try:
        file = controller.form_images.get_file_path(db, name)
        if file is None:
            return JSONResponse(content={'data': {'name': None}})
        base_path = f"{settings.NFS_PATH}{file.path}"
        if os.path.exists(base_path):
            return FileResponse(base_path)
        return JSONResponse(content={'data': {'name': None}})

    except Exception as e:
        print(e)


@router.get("/{form_id}")
def download_zip_file(
        form_id: str,
        db: Session = Depends(deps.get_db),
        current_user: models.Users = Depends(deps.get_current_active_referee_or_admin),
) -> Any:
    """
    Download Files as a zip.
    """
    file = controller.form.get_files(db, form_id=form_id)
    if file is None:
        return JSONResponse(content={'data': {'name': None}})
    return FileResponse(file, media_type='application/x-zip-compressed', filename=file.split('/')[-1])
