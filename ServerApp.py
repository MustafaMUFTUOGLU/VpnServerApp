import asyncio

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from RabbitmqClient import RabbitmqClient
from api.v1.api import api_router
from core.config import settings
from db.database import SessionLocal
# from socket_io import sio

import socketclient
from socketclient.SocketManager import SocketManager

# import sys

# # 👇️ 1000
# print(sys.getrecursionlimit())

# # 👇️ set recursion limit to 2000
# sys.setrecursionlimit(5000)

# # 👇️ 2000
# print(sys.getrecursionlimit())


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

app.include_router(api_router, prefix=settings.API_V1_STR)

# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

socketapp = SocketManager(app)

app.mount("/socket.io", socketapp.getApp())

rabbitmqapp = RabbitmqClient(app)
@app.on_event("startup")
async def on_startup():
    await rabbitmqapp.connect()
    # app.rabbitmq_connection = await connect_rabbitmq()
    # asyncio.create_task(listen_for_user_device(app.rabbitmq_connection, cluster))
    # asyncio.create_task(listen_for_device_user(app.rabbitmq_connection, cluster))


@app.on_event("shutdown")
async def on_shutdown():
    await app.rabbitmq_connection.close()