import base64
import json
from datetime import datetime
from typing import Any, List
from fast_captcha import img_captcha
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import hashlib
from utils import generate_random_string, send_new_account_email
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse
import controller
import schemas
from api import deps
from core.app import redis_cache

router = APIRouter()


@router.get("", response_model=List[schemas.Group])
def captcha(
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Captcha
    """
    img, text = img_captcha(font_type='fonts/BY-Easy-love-2.ttf')

    data = base64.b64encode(img.getvalue())

    m = hashlib.sha1()
    m.update(data)
    hash = m.hexdigest()

    redis_cache.add_to_cache(key=hash, value={'captcha': text, 'data': data.decode('utf-8')}, expire=300)
    return StreamingResponse(content=img, media_type='image/jpeg')


@router.post("", response_model=schemas.Otp)
def check_email(
        otp: schemas.Otp,
        db: Session = Depends(deps.get_db),
) -> Any:
    """
    Check email domain
    """
    m = hashlib.sha1()
    m.update(otp.img.encode('utf-8'))
    hash = m.hexdigest()

    # redis_check = redis_cache.check_cache(key=hash)
    # if not redis_check or len(redis_check) < 2 or redis_check[1] is None:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Geçersiz captcha",
    #     )

    # redis_data = json.loads(redis_check[1].decode('utf-8'))

    # if redis_data['captcha'] != otp.recaptcha:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Geçersiz captcha",
    #     )

    user = controller.user.get_by_email(db, email=otp.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Bu email adresi ile daha önce kayıt olunmuş",
        )

    check_otp = controller.otp.get_by_email(db, email=otp.email)

    # approved_email = controller.approved_email.check_email(db, email_domain=otp.email.split('@')[1],
    #                                                        corporation=otp.corporation)
    # if approved_email is None:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="Mail adresi ile kurum eşleşmiyor",
    #     )

    otp.otp = generate_random_string(6)
    otp.create_time = datetime.now()

    del otp.recaptcha
    del otp.img
    if not check_otp:
        otp = controller.otp.create(db, obj_in=otp)
    else:
        otp_update = jsonable_encoder(otp)
        otp.uuid = check_otp.uuid
        otp_update['uuid'] = check_otp.uuid
        otp_update['otp'] = otp.otp
        otp_update['create_time'] = otp.create_time
        controller.otp.update(db, db_obj=check_otp, obj_in=otp_update)
   
    send_new_account_email(
        email=otp.email, otp=otp.otp
    )

    redis_cache.redis.getdel(name=hash)
    del otp.otp
    return JSONResponse(content={'data': jsonable_encoder(otp)})


@router.post("/otp-verify/", response_model=schemas.TokenMessage)
def otp_verify(
        email: str = Body(...),
        otp: str = Body(...),
        recaptcha: str = Body(...),
        img: str = Body(...),
        db: Session = Depends(deps.get_db)
) -> Any:
    """
    OTP Verification
    """
    m = hashlib.sha1()
    m.update(img.encode('utf-8'))
    recaptcha_hash = m.hexdigest()

    redis_check = redis_cache.check_cache(key=recaptcha_hash)
    if not redis_check or len(redis_check) < 2 or redis_check[1] is None:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz captcha",
        )

    redis_data = json.loads(redis_check[1].decode('utf-8'))

    if redis_data['captcha'] != recaptcha:
        raise HTTPException(
            status_code=400,
            detail="Geçersiz captcha",
        )

    otp = controller.otp.check_otp(db, email=email, otp=otp)
    if not otp:
        raise HTTPException(
            status_code=401,
            detail="Geçersiz email adresi veya OTP",
        )

    otp_update = jsonable_encoder(otp)
    otp_update['status'] = True

    controller.user.update(db, db_obj=otp, obj_in=otp_update)

    m = hashlib.sha1()
    m.update(otp.otp.encode('utf-8'))
    hash = m.hexdigest()

    redis_cache.redis.getdel(name=recaptcha_hash)
    return {"msg": "OTP doğrulama başarılı", "hash": hash}
