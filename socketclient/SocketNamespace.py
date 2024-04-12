import socketio

from api.deps import controlUser
from db.database import SessionLocal


class PublicNamespace(socketio.AsyncNamespace):

    def __init__(self, path, app, sio):
        super().__init__(path)
        self.app = app
        self.sio = sio

    async def on_connect(self, sid, environ):
        print("on connect")
        self.sid = sid
        pass

    async def on_disconnect(self, sid):
        print("on_disconnect")
        pass

    async def on_my_event(self, sid, data):
        print("----- on_my_event")
        await self.emit('my_response', data)

    async def sendMessage(self, msg):
        await self.emit('message', msg, self.sid)

        print("sendmessage", msg)

    async def on_login(self, sid, msg):
        print(f"login {msg}")
        db = SessionLocal()
        user = controlUser(db, msg)
        print(f"userid: ", user.uuid)
        _client = PrivateNamespace(f"/{str(user.uuid)}")
        self.app.socket_clients[f"{user.uuid}"] = _client
        self.sio.register_namespace(_client)
        await self.sio.emit("access", str(user.uuid), room=sid)  # we can send message to specific sid


class PrivateNamespace(socketio.AsyncNamespace):
    async def on_connect(self, sid, environ):
        print("----- on connect")
        self.sid = sid
        pass

    async def on_disconnect(self, sid):
        print("----- on_disconnect")
        pass

    async def on_my_event(self, sid, data):
        print("----- on_my_event")
        await self.emit('my_response', data)

    async def sendMessage(self, msg):
        await self.emit('message', msg, self.sid)

        print("sendmessage", msg)
