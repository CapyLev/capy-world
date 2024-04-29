import ujson
from aio_pika.abc import AbstractIncomingMessage
from sanic import Websocket
from sanic.log import logger

from src.modules.realm.daos import MessageDAO
from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    ConnectToServerService,
)
from src.utils.singlton_meta import SingletonMeta


class _ConnectionManager(metaclass=SingletonMeta):
    # TODO: на подумать. Dict[server_id: Dict[uuid: Dict[user_id: WS_CONN]]]
    # _connections: dict[int, dict[str, dict[int, Websocket]]] = {}
    _connections: dict[int, set[Websocket]] = {}

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
    ) -> None:
        if server_id not in self._connections:
            self._connections[server_id] = set()

        self._connections[server_id].add(ws)
        await self._connect_to_server_service.execute(server_id)

    async def disconnect(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None:
        server = self._connections.get(server_id, set())

        try:
            server.remove(ws)
        except KeyError:
            logger.warning(f'Server {server_id} has no connections for user {user_id}')
            return

        await self._disconnect_from_server_service.execute()

    async def broadcast(
        self,
        message: AbstractIncomingMessage,
    ) -> None:
        try:
            server_id = ujson.loads(message.body.decode(encoding='utf-8', errors='strict'))['server_id']
        except (ValueError, KeyError) as exc:
            logger.error(f"Error decoding incoming ws message or retrieving server_id: Error {str(exc)}")
            return

        for ws_connection in self._connections.get(server_id, set()):
            try:
                await ws_connection.send(message.body)
            except Exception as exc:
                logger.error(f"Error sending message through WebSocket: {exc}")


ConnectionManager: _ConnectionManager = _ConnectionManager(
    connect_to_server_service=ConnectToServerService(
        message_dao=MessageDAO(),
    ),
    disconnect_from_server_service=DisconnectFromServerService(),
    broadcast_service=BroadcastService(),
)
