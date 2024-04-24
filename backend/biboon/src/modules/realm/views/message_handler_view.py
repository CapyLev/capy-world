import logging
from datetime import datetime

import ujson
from sanic import Request, Websocket
from websockets import exceptions

from config.message_transmitter import RabbitMQTransmitter, MessageDTO
from src.modules.realm.repository import MessageRepository
from src.modules.realm.connection_manager import ConnectionManager
from src.modules.realm.services import (
    HandleIncomingWSMessagesService,
    ConnectToServerService,
    DisconnectFromServerService,
    BroadcastService,
)

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

    # TODO: own ws protocol with async iter to use `async for`

    try:
        while True:
            msg = await ws.recv()

            try:
                await service.execute(MessageDTO(**ujson.loads(msg)))
            except ujson.JSONDecodeError:
                logger.exception(f"Error decoding ws message: {msg}", extra={
                    'server_id': server_id,
                    'user_id': user_id,
                    'message': msg,
                    'exception_datetime': datetime.now().isoformat(),
                })
    except exceptions.ConnectionClosedOK as exc:
        pass
    except exceptions.ConnectionClosed as exc:
        logger.exception(f'Connection closed: {exc}', extra={
            'server_id': server_id,
            'user_id': user_id,
            'exception_datetime': datetime.now().isoformat(),
        })
        await ConnectionManager.disconnect(
            ws=ws,
            server_id=server_id,
            user_id=user_id,
        )
        # TODO: handle offline status
    except Exception as exc:
        logger.critical(f'Unexpected exception: {exc}', extra=exc.__dict__)
