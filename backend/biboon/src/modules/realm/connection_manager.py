import ujson
from aio_pika.abc import AbstractIncomingMessage
from sanic import Websocket

from src.modules.realm.repository import MessageRepository
from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    ConnectToServerService,
)


class _ConnectionManager:
    _connections: dict[int, dict[int, Websocket]] = {}

    def __init__(
        self,
        connect_to_server_service: ConnectToServerService,
        disconnect_from_server_service: DisconnectFromServerService,
        broadcast_service: BroadcastService,
    ) -> None:
        self._connect_to_server_service = connect_to_server_service
        self._disconnect_from_server_service = disconnect_from_server_service
        self._broadcast_service = broadcast_service

    async def connect(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None:
        if server_id not in self._connections:
            self._connections[server_id] = {}
        self._connections[server_id][user_id] = ws

        await self._connect_to_server_service.execute(ws, server_id, user_id)

    async def disconnect(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None: ...

    async def broadcast(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        decoded_message = ujson.loads(message.body.decode(encoding='utf-8', errors='strict'))
        pool_of_server_connections = self._connections[decoded_message['server_id']]

        for _, ws_connection in pool_of_server_connections.items():
            await ws_connection.send(decoded_message)


ConnectionManager: _ConnectionManager = _ConnectionManager(
    connect_to_server_service=ConnectToServerService(
        message_repository=MessageRepository(),
    ),
    disconnect_from_server_service=DisconnectFromServerService(),
    broadcast_service=BroadcastService(),
)
