import socketio


class PublicNamespace(socketio.AsyncNamespace):
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

    async def login(self, sid, msg):
        print(f"login {msg}")
        db = SessionLocal()
        user = controlUser(db, msg)
        print(f"userid: ", user.uuid);
        _cluster = MyCustomNamespace(f"/{str(user.uuid)}")
        cluster[f"{user.uuid}"] = _cluster
        sio.register_namespace(_cluster)
        await sio.emit("access", str(user.uuid), room=sid)  # we can send message to specific sid

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
