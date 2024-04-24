import ujson
from sanic import Request, Websocket

from config.message_transmitter import RabbitMQTransmitter, MessageDTO
from src.modules.realm.repository import MessageRepository
from src.modules.realm.connection_manager import ConnectionManager
from src.modules.realm.services import (
    HandleIncomingWSMessagesService,
    ConnectToServerService,
    DisconnectFromServerService,
    BroadcastService,
)


async def message_handler_view(
    _: Request,
    ws: Websocket,
    server_id: int,
    user_id: int,
):
    connection_manager = ConnectionManager(
        connect_to_server_service=ConnectToServerService(
            message_repository=MessageRepository(),
        ),
        disconnect_from_server_service=DisconnectFromServerService(),
        broadcast_service=BroadcastService(),
    )

    await connection_manager.connect(
        ws=ws,
        user_id=user_id,
        server_id=server_id,
    )

    service = HandleIncomingWSMessagesService(
        message_repository=MessageRepository(),
        message_transmitter=RabbitMQTransmitter(),
    )

    async for msg in ws:
        await service.execute(MessageDTO(**ujson.loads(msg)))
