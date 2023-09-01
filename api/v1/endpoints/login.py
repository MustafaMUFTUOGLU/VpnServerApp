import hashlib
import json
from datetime import timedelta, datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import controller
import schemas
from api import deps
from core import security
from core.app import redis_cache
from core.config import settings
from core.security import get_password_hash
from schemas import UserRoles
from utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
    send_updated_password_email,
    send_let_me_know_email,
)

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login_access_token(
        db: Session = Depends(deps.get_db),
        login_data: schemas.Login = Body()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    redis_key = 'login:' + login_data.email
    redis_check = redis_cache.check_cache(key=redis_key)

    if len(redis_check) >= 2 and redis_check[1] is not None:
        redis_cache.add_to_cache(key=redis_key, value=int(redis_check[1]) + 1, expire=settings.LOGIN_RETRY_TTL)
        if int(redis_check[1]) >= 5:
            if int(redis_check[1]) % 5 == 0:
                for mail in settings.LET_ME_KNOW_LIST['mails']:
                    send_let_me_know_email(
                        email=mail,
                        environment={
                            "project_name": settings.PROJECT_NAME,
                            "project_url": settings.SERVER_HOST,
                            "email": login_data.email,
                        }
                    )
            raise HTTPException(status_code=400,
                                detail="Çok fazla hatalı giriş denemesi yaptınız. " + str(
                                    settings.LOGIN_RETRY_TTL) + " saniye sonra tekrar deneyiniz.")
    else:
        redis_cache.add_to_cache(key=redis_key, value=0, expire=settings.LOGIN_RETRY_TTL)

    m = hashlib.sha1()
    m.update(login_data.img.encode('utf-8'))
    hash = m.hexdigest()

    redis_check = redis_cache.check_cache(key=hash)
    if not redis_check or len(redis_check) < 2 or redis_check[1] is None:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz captcha",
        )

    redis_data = json.loads(redis_check[1].decode('utf-8'))

    if redis_data['captcha'] != login_data.recaptcha:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz captcha",
        )

    user = controller.user.authenticate(db, email=login_data.email, password=login_data.password)
    if not user:
        print(f'Hatalı Kullanıcı Girişi:{login_data.email}')
        raise HTTPException(status_code=400, detail="Hatalı email adresi veya şifre")
    elif not controller.user.is_active(user):
        raise HTTPException(status_code=400, detail="2. aşamaya geçmeye hak kazanamadınız.")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            {
                "user_uuid": user.uuid,
                "status": user.status,
                "email": user.email,
                "role": user.users_roles[0].roles.name,
                "name": user.name,
                "surname": user.surname
            }, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/oauth", response_model=schemas.Token)
def login_oauth(
        db: Session = Depends(deps.get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = controller.user.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Hatalı email adresi veya şifre")
    elif not controller.user.is_active(user):
        raise HTTPException(status_code=400, detail="Kullanıcı aktif değil")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            {
                "user_uuid": user.uuid,
                "status": user.status,
                "email": user.email,
                "role": user.users_roles[0].roles.name,
                "name": user.name,
                "surname": user.surname
            }, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-recovery/{email}")
def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = controller.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kullanıcı sistemde bulunamadı",
        )

    redis_key = 'password-recovery:' + email
    redis_check = redis_cache.check_cache(key=redis_key)
    if len(redis_check) >= 2 and redis_check[1] is not None:
        raise HTTPException(
            status_code=400,
            detail="1 dakika içinde 2 kez şifre sıfırlama talebinde bulunamazsınız",
        )

    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email=email, name=user.name, surname=user.surname, token=password_reset_token
    )
    redis_cache.add_to_cache(key=redis_key, value=email, expire=60)
    return {"msg": "Şifre sıfırlama linki mail adresinize gönderildi"}


@router.post("/reset-password/")
def reset_password(
        token: str = Body(...),
        new_password: str = Body(...),
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Geçersiz token")
    user = controller.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Kullanıcı sistemde bulunamadı",
        )
    elif not controller.user.is_active(user):
        raise HTTPException(status_code=400, detail="Kullanıcı aktif değil")
    hashed_password = get_password_hash(new_password)
    user.password = hashed_password
    db.add(user)
    db.commit()

    send_updated_password_email(
        email=email, name=user.name, surname=user.surname
    )
    return {"msg": "Şifreniz başarıyla güncellendi"}


@router.post("/register", response_model=schemas.Register)
def create_user(
        register: schemas.Register,
        db: Session = Depends(deps.get_db),

) -> Any:
    """
    Create new user.
    """
    user = controller.user.get_by_email(db, email=register.user.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Kullanıcı sistemde bulunmaktadır: " + user.email,
        )

    check_otp = controller.otp.get_by_email(db, email=register.user.email)
    if not check_otp:
        raise HTTPException(
            status_code=400,
            detail="OTP doğrulaması yapan email ile kayıt işlemi yapan email adresi aynı olmalıdır",
        )

    m = hashlib.sha1()
    m.update(check_otp.otp.encode('utf-8'))
    check_otp_hash = m.hexdigest()

    if register.hash != check_otp_hash:
        raise HTTPException(
            status_code=400,
            detail="OTP doğrulaması başarısız olduğundan kayıt işlemi gerçekleştirilemedi",
        )

    # if register.group is not None:
    #     for group in register.group:
    #         group_check = controller.group.get_by_email(db, email=group.email)
    #         if group_check:
    #             raise HTTPException(
    #                 status_code=400,
    #                 detail="Kullanıcı başka bir grubta bulunmaktadır: " + group_check.email,
    #             )

    password = register.user.password
    register.user.password = get_password_hash(password)
    register.user.create_time = datetime.utcnow()
    register.user.last_update_time = datetime.utcnow()
    register.user.status = True
    user = controller.user.create(db, obj_in=register.user)

    get_role = controller.role.find_by_name(db, name='user')

    user_role = UserRoles(
        user_uuid=user.uuid,
        role_uuid=get_role.uuid,
        create_user=user.uuid,
        last_update_user=user.uuid,
    )
    controller.user_role.create(
        db, obj_in=user_role
    )

    if register.group is not None:
        for group in register.group:
            group.group_name = register.group_name
            group.create_user = user.uuid
            group.last_update_user = user.uuid
            inserted_group = controller.group.create(db, obj_in=group)
            group.uuid = inserted_group.uuid

    register.user.uuid = user.uuid
    del register.user.password
    return JSONResponse(content={'data': jsonable_encoder(register)})
