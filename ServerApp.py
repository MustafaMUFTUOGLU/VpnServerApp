from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.config import settings

if settings.FAST_API == 'dev':
    docs_url = '/docs'
    redoc_url = '/redoc'
    openapi_url = f"{settings.API_V1_STR}/openapi.json"
else:
    docs_url = None
    redoc_url = None
    openapi_url = None

app = FastAPI(
    title=settings.PROJECT_NAME, docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

