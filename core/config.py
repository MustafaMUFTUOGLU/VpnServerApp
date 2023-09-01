import os
import secrets
from typing import Any, Dict, List, Optional, Union
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


class Settings(BaseSettings):
    load_dotenv()
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_HOST = os.environ.get('SERVER_HOST')
    FAST_API = os.environ.get('FAST_API')
    # SERVER_NAME: str
    # SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS = os.environ.get('BACKEND_CORS_ORIGINS')
    # ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS')

    MIME_TYPES = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif', 'application/pdf', 'application/msword',
                  'application/vnd.ms-excel',
                  'application/vnd.ms-powerpoint',
                  'video/mp4', 'video/mpeg',
                  'video/quicktime', 'audio/mpeg',
                  'audio/x-m4a',
                  'audio/mp3']

    FILE_EXTENTIONS = ['jpeg', 'jpg', 'png', 'gif', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'mp4', 'm4a',
                       'mpeg', 'mov', 'avi', 'mp3']

    BACKEND_CORS_ORIGINS = ["*"]

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME = os.environ.get('PROJECT_NAME')
    # SENTRY_DSN: Optional[HttpUrl] = None
    #
    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    DATABASE_URI = os.environ.get('DATABASE_URI')
    END_DATE = os.environ.get('END_DATE')

    IS_RELAY: bool = os.environ.get('IS_RELAY')
    SMTP_TLS: bool = os.environ.get('SMTP_TLS')
    SMTP_PORT: int = os.environ.get('SMTP_PORT')
    SMTP_HOST: str = os.environ.get('SMTP_HOST')
    SMTP_USER: str = os.environ.get('SMTP_USER')
    SMTP_DEBUG: str = os.environ.get('SMTP_DEBUG')
    SMTP_PASSWORD: str = os.environ.get('SMTP_PASSWORD')
    EMAILS_FROM_EMAIL: EmailStr = os.environ.get('EMAILS_FROM_EMAIL')
    EMAILS_FROM_NAME: str = PROJECT_NAME
    Token: str = os.environ.get('Token')
    #NFS_PATH: str = os.environ.get('NFS_PATH')
    REPORT_MAIL_LIST: Dict = os.environ.get('REPORT_MAIL_LIST')

    LET_ME_KNOW_LIST: Dict = os.environ.get('LET_ME_KNOW_LIST')
    LOGIN_RETRY_TTL: int = os.environ.get('LOGIN_RETRY_TTL')

    basedir = os.path.abspath(os.path.dirname(__file__))
    EMAIL_TEMPLATES_DIR: str = basedir + "/../templates"

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 24
    EMAILS_ENABLED: bool = False

    CACHE_REDIS_URL: str = os.environ.get('CACHE_REDIS_URL')
    CACHE_TYPE: str = os.environ.get('CACHE_TYPE')

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
