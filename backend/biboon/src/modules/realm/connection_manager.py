import ujson
from aio_pika.abc import AbstractIncomingMessage
from sanic import Websocket
from sanic.log import logger

from config.message_transmitter import MessageDTO
from src.modules.realm.daos import MessageDAO
from src.modules.realm.services import (
    BroadcastService,
    DisconnectFromServerService,
    SendLastMessagesToServerService,
)
from src.utils.singlton_meta import SingletonMeta


class _ConnectionManager(metaclass=SingletonMeta):
    _connections: dict[int, set[Websocket]] = {}

    def __init__(
        self,
        send_last_messages_to_server_service: SendLastMessagesToServerService,
        disconnect_from_server_service: DisconnectFromServerService,
        broadcast_service: BroadcastService,
    ) -> None:
        self._send_last_messages_to_server_service = (
            send_last_messages_to_server_service
        )
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
        last_server_messages = await self._send_last_messages_to_server_service.execute(
            server_id=server_id
        )
        [await self.broadcast(last_message) for last_message in last_server_messages]

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
            logger.warning(f"Server {server_id} has no connections for user {user_id}")
            return

        await self._disconnect_from_server_service.execute()

    async def broadcast(
        self,
        message: AbstractIncomingMessage | MessageDTO,
    ) -> None:
        if isinstance(message, AbstractIncomingMessage):
            message_body = message.body.decode(encoding="utf-8")
        elif isinstance(message, MessageDTO):
            message_body = message.model_dump_json()
        else:
            logger.error(f"Invalid message type: {type(message)}")
            return

        try:
            server_id = ujson.loads(message_body)["server_id"]
        except (ValueError, KeyError) as exc:
            logger.error(
                f"Error decoding incoming ws message or retrieving server_id: Error {str(exc)}"
            )
            return

        for ws_connection in self._connections.get(server_id, set()):
            try:
                await ws_connection.send(message_body)
            except Exception as exc:
                logger.error(f"Error sending message through WebSocket: {exc}")


ConnectionManager: _ConnectionManager = _ConnectionManager(
    send_last_messages_to_server_service=SendLastMessagesToServerService(
        message_dao=MessageDAO(),
    ),
    disconnect_from_server_service=DisconnectFromServerService(),
    broadcast_service=BroadcastService(),
)
