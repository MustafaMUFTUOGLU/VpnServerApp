import logging
import random
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from core.config import settings


def send_email(
        email: str,
        subject_template: str = "",
        html_template: str = "",
        environment: Dict[str, Any] = {},
        file: str = None
) -> None:
    print("-----------------")
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    print("+++++++++++++++++")
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    if file:
        message.attach(data=open(file), filename=file.split('/')[-1])
        message.text = ' '
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT, "debug": int(settings.SMTP_DEBUG)}
    if not settings.IS_RELAY:
        if settings.SMTP_TLS:
            smtp_options["tls"] = True
        if settings.SMTP_USER:
            smtp_options["user"] = settings.SMTP_USER
        if settings.SMTP_PASSWORD:
            smtp_options["password"] = settings.SMTP_PASSWORD
    print("-----------------")
    response = message.send(to=email, render=environment, smtp=smtp_options)
    print(f"***************** {response}")
    logging.info(f"send email result: {response}")


def send_reset_password_email(email: str, name: str, surname: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Şifre Sıfırlama Talebi"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "password-recovery.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "project_url": server_host,
            "email": email,
            "name": name,
            "surname": surname,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link
        },
    )


def send_updated_password_email(email: str, name: str, surname: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Şifreniz Sıfırlandı"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "password-updated.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    send_email(
        email=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "project_url": server_host,
            "email": email,
            "name": name,
            "surname": surname
        },
    )


def send_let_me_know_email(email: str, environment: dict) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Hatalı Giriş Denemesi!"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "let-me-know.html") as f:
        template_str = f.read()
    send_email(
        email=email,
        subject_template=subject,
        html_template=template_str,
        environment=environment,
    )


def send_new_account_email(email: str, name: str = "", surname: str = "", otp: str = "", role: str = "",
                           password: str = "") -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Mail Hesabınızı Doğrulayın"
    server_host = settings.SERVER_HOST
    link = f"{server_host}"
    if role == "referee":
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new-account-otp-referee.html") as f:
            template_str = f.read()
    else:
        with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new-account-otp.html") as f:
            template_str = f.read()
    send_email(
        email=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "project_url": server_host,
            "name": name,
            "surname": surname,
            "email": email,
            "otp": otp,
            "link": link,
            "password": password
        },
    )


def send_new_referee_mail(email: str, name: str = "", surname: str = "", form_name: str = ""):
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Form Değerlendirme Ataması"
    server_host = settings.SERVER_HOST
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new-referee-form.html") as f:
        template_str = f.read()
    send_email(
        email=email,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "project_url": server_host,
            "name": name,
            "surname": surname,
            "form_name": form_name,
            "link": server_host
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def generate_password(length):
    punctuation = '!#$%&()*+-./:<=>?@[]_{|}~'
    ascii1 = [random.choice(string.ascii_letters) for n in range(2)]
    digit = [random.choice(string.digits) for n in range(2)]
    punc = [random.choice(punctuation) for n in range(2)]
    ascii2 = [random.choice(string.ascii_letters) for n in range(length - 6)]
    return ''.join(ascii1 + digit + punc + ascii2)

