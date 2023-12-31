from __future__ import annotations

import websockets
import logging 

import asyncio
from typing import (
    Tuple,
    Optional,
    Any,
    cast
)

from fastapi import status


from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from websocket.messagemodel.messages import MessageModel


class ConnectionError(Exception):
    pass


class ConnectionManagerNotStarted(ConnectionError):
    pass


class ConnMgr:

    _is_incoming_started: bool
    _incoming_queue: asyncio.Queue[Tuple[IncomingConnection, MessageModel]]

    def __init__(self):
        self._is_incoming_started = False
        self._incoming_queue = asyncio.Queue()

    def start_receiving(self) -> None:
        self._is_incoming_started = True

    def is_started(self) -> bool:
        return self._is_incoming_started

    async def on_incoming_receive(
        self,
        conn: IncomingConnection,
        msg: MessageModel
    ) -> None:
        logging.debug(f"connmgr -- incoming recv: {conn}, {msg}")

        if not self.is_started():
            raise ConnectionManagerNotStarted()

        await self._incoming_queue.put((conn, msg))
        logging.debug(f"connmgr -- queue len: {self._incoming_queue.qsize()}")

    async def wait_incoming_msg(
        self
    ) -> Tuple[IncomingConnection, MessageModel]:
        return await self._incoming_queue.get()

    async def connect(self, endpoint: str) -> OutgoingConnection:
        wsclient = await websockets.connect(endpoint)
        conn = OutgoingConnection(wsclient)
        return conn
    
class IncomingConnection(WebSocketEndpoint):

    _ws: Optional[WebSocket] = None

    async def on_connect(self, websocket: WebSocket) -> None:
        logging.debug(f"incoming -- from {websocket.client}")

        connmgr: ConnMgr = get_conn_mgr()
        if not connmgr.is_started():
            await websocket.close(status.WS_1013_TRY_AGAIN_LATER)
            return

        self._ws = websocket
        await websocket.accept()

    async def on_disconnect(
        self,
        websocket: WebSocket,
        close_code: int
    ) -> None:
        logging.debug(f"incoming -- disconnect from {websocket.client}")
        self._ws = None

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        logging.debug(f"incoming -- recv from {websocket.client}: {data}")
        connmgr: ConnMgr = get_conn_mgr()
        assert connmgr.is_started()
        msg: MessageModel = MessageModel.parse_raw(data)
        await connmgr.on_incoming_receive(self, msg)

    async def send_msg(self, data: MessageModel) -> None:
        logging.debug(f"incoming -- send to {self._ws} data {data}")
        assert self._ws
        await self._ws.send_text(data.json())

    @property
    def address(self) -> str:
        assert self._ws
        return cast(str, self._ws.client.host)  
    
class OutgoingConnection:
    _ws: websockets.WebSocketClientProtocol

    def __init__(self, ws: websockets.WebSocketClientProtocol) -> None:
        self._ws = ws

    async def send(self, msg: MessageModel) -> None:
        assert self._ws
        await self._ws.send(msg.json())

    async def receive(self) -> MessageModel:
        assert self._ws
        raw = await self._ws.recv()
        return MessageModel.parse_raw(raw)

    async def close(self) -> None:
        assert self._ws
        await self._ws.close()


_connmgr = ConnMgr()


def get_conn_mgr() -> ConnMgr:
    return _connmgr