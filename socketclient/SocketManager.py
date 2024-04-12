from .SocketNamespace import PublicNamespace
from socketio import ASGIApp, AsyncServer


class SocketManager():
    def __init__(self, app):
        app.socket_clients = {}
        self.sio = AsyncServer(async_mode="asgi", cors_allowed_origins=[], cors_credentials=True)
        self.socket_app = ASGIApp(socketio_server=self.sio, socketio_path='/')
        self.sio.register_namespace(PublicNamespace('/', app, self.sio))
    def getApp(self):
        return self.socket_app



