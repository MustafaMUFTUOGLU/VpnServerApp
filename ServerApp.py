from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from api.v1.api import api_router
from core.config import settings
# from websocket.wbsocket import IncomingConnection
from websocket.sioservice import StudyNamespace
import socketio

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

sio = socketio.AsyncServer(async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

app = FastAPI(
    # title=settings.PROJECT_NAME, docs_url=docs_url, redoc_url=redoc_url, openapi_url=openapi_url
)


@app.get("/test")
async def test():
    print("test")
    return "WORKS"

app.mount("/", socket_app)

@sio.on("connect")
async def connect(sid, env):
    print("on connect")


@sio.on("direct")
async def direct(sid, msg):
    print(f"direct {msg}")
    await sio.emit("event_name", msg, room=sid)  # we can send message to specific sid


@sio.on("broadcast")
async def broadcast(sid, msg):
    print(f"broadcast {msg}")
    await sio.emit("event_name", msg)  # or send to everyone


@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")



# Set all CORS enabled origins
# if settings.BACKEND_CORS_ORIGINS:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"],
#     )

# app.include_router(api_router, prefix=settings.API_V1_STR)

# sio = socketio.AsyncServer(
#     async_mode           = 'asgi',
#     cors_allowed_origins = '*',
#     debug                = False
# )

# def handle_connect():
#     print("handle_connect")

# sio.on("connect", handler=handle_connect)


# sio.register_namespace(StudyNamespace(sio, '/study'))


# sio_app = socketio.ASGIApp(socketio_server=sio, other_asgi_app=app)
 
# app.mount("/ws", sio_app )

