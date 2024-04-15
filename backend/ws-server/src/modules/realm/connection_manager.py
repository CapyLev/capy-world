from fastapi import WebSocket

from src.modules.message_transmitter.interfaces import (
    MessageTransmitter,
    TransmitterMessageDTO,
)


class ConnectionManager:
    connections: dict[int, dict[int, WebSocket]] = {}

    def __init__(
        self,
        message_transmitter: MessageTransmitter,
        connect_to_server_service: ...,
        disconnect_from_server_service: ...,
        broadcast_service: ...,
    ) -> None:
        self._message_transmitter = message_transmitter

    async def connect(self, ws: WebSocket, server_id: int, user_id: int) -> None: ...

    async def disconnect(self, ws: WebSocket, server_id: int, user_id: int) -> None: ...

    async def broadcast(
        self,
        ws: WebSocket,
        server_id: int,
        user_id: int,
        message: TransmitterMessageDTO,
    ) -> None: ...
