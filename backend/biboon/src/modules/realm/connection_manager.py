import ujson
from aio_pika.abc import AbstractIncomingMessage
from sanic import Websocket
from sanic.log import logger

from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    ConnectToServerService,
)
from src.utils.singlton_meta import SingletonMeta


class ConnectionManager(metaclass=SingletonMeta):
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
        logger.debug(f"TEST Broadcasting message: {message.body}")
        logger.debug(f"TEST Broadcasting message: {message.content_type}")

        try:
            server_id = ujson.loads(message.body.decode(encoding='utf-8', errors='strict'))['server_id']
        except (ValueError, KeyError) as exc:
            logger.error(f"Error decoding incoming ws message or retrieving server_id: Error {str(exc)}")
            return

        try:
            pool_of_server_connections = self._connections[server_id]
        except KeyError:
            logger.error(f"No connections available for server_id: {server_id}")
            return

        for _, ws_connection in pool_of_server_connections.items():
            try:
                await ws_connection.send(message.body)
            except Exception as e:
                logger.error(f"Error sending message through WebSocket: {str(e)}")
