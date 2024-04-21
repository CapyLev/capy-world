from sanic import Websocket

from config import (
    rabbitmq_transmitter,
    MessageTransmitter,
    MessageDTO,
)
from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    ConnectToServerService,
)


class ConnectionManager:
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
    ) -> None: ...

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


connection_manager: ConnectionManager = ConnectionManager(
    message_transmitter=rabbitmq_transmitter,
    connect_to_server_service=ConnectToServerService(),
    disconnect_from_server_service=DisconnectFromServerService(),
    broadcast_service=BroadcastService(),
)
