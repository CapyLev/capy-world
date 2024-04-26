import logging
from datetime import datetime

from sanic import Request, Websocket
from websockets import exceptions

from config.message_transmitter import RabbitMQTransmitter
from src.modules.realm.repository import MessageRepository
from src.modules.realm.connection_manager import ConnectionManager
from src.modules.realm.services import HandleIncomingWSMessagesService

logger = logging.getLogger(__name__)


async def message_handler_view(
    _: Request,
    ws: Websocket,
    server_id: int,
    user_id: int,
):
    await ConnectionManager.connect(
        ws=ws,
        user_id=user_id,
        server_id=server_id,
    )

    service = HandleIncomingWSMessagesService(
        message_repository=MessageRepository(),
        message_transmitter=RabbitMQTransmitter(),
    )

    should_close_connection = False
    try:
        while True:
            logger.exception(f'connected user {ConnectionManager._connections}')
            should_close_connection = await service.execute(
                message_from_connection=await ws.recv(),
            )
    except exceptions.ConnectionClosedOK as exc:
        logger.critical(f'Connection closed from client: {exc}')
        should_close_connection = True
    except exceptions.ConnectionClosed as exc:
        logger.exception(f'Connection closed: {exc}', extra={
            'server_id': server_id,
            'user_id': user_id,
            'exception_datetime': datetime.now().isoformat(),
        })
        should_close_connection = True
    except Exception as exc:
        logger.critical(f'Unexpected exception: {exc}')
        should_close_connection = True

    if should_close_connection:
        await ConnectionManager.disconnect(
            ws=ws,
            server_id=server_id,
            user_id=user_id,
        )
