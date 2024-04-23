from sanic import Websocket

from config.message_transmitter import (
    RabbitMQTransmitter,
    MessageTransmitter,
    MessageDTO,
)
from src.modules.realm.repository import MessageRepository
from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    ConnectToServerService,
)


class _ConnectionManager:
    connections: dict[int, dict[int, Websocket]] = {}

    def __init__(
        self,
        message_transmitter: MessageTransmitter,
        connect_to_server_service: ConnectToServerService,
        disconnect_from_server_service: DisconnectFromServerService,
        broadcast_service: BroadcastService,
    ) -> None:
        self._message_transmitter = message_transmitter
        self._connect_to_server_service = connect_to_server_service
        self._disconnect_from_server_service = disconnect_from_server_service
        self._broadcast_service = broadcast_service

    async def connect(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None:
        if server_id not in self.connections:
            self.connections[server_id] = {}
        self.connections[server_id][user_id] = ws

        await self._connect_to_server_service.execute(ws, server_id, user_id)

    async def disconnect(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None: ...

    async def broadcast(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
        message: MessageDTO,
    ) -> None: ...


ConnectionManager: _ConnectionManager = _ConnectionManager(
    message_transmitter=RabbitMQTransmitter,
    connect_to_server_service=ConnectToServerService(
        message_repository=MessageRepository(),
    ),
    disconnect_from_server_service=DisconnectFromServerService(),
    broadcast_service=BroadcastService(),
)
