import asyncio
import logging
from datetime import datetime

from sanic import Request, Websocket
from websockets import exceptions

from config import constants
from config.message_transmitter import RabbitMQTransmitter
from src.modules.realm.daos import MessageDAO
from src.modules.realm.connection_manager import ConnectionManager
from src.modules.realm.services import HandleIncomingWSMessagesService

logger = logging.getLogger(__name__)


async def message_handler_view(
    _: Request,
    ws: Websocket,
    server_id: int,
    user_id: int,
):
    await ConnectionManager.connect(ws=ws, server_id=server_id)

    message_service = HandleIncomingWSMessagesService(
        message_dao=MessageDAO(),
        message_transmitter=RabbitMQTransmitter(),
    )

    used_retries = 0
    while True:
        try:
            message = await ws.recv()
            await message_service.execute(message_from_connection=message)
            used_retries = 0
        except exceptions.ConnectionClosedOK as exc:
            logger.critical(f"Connection closed from client: {exc}")
            break
        except exceptions.ConnectionClosed as exc:
            logger.exception(
                f"Connection closed: {exc}",
                extra={
                    "server_id": server_id,
                    "user_id": user_id,
                    "exception_datetime": datetime.now().isoformat(),
                },
            )
            if used_retries >= constants.server.WEBSOCKET_MAX_RETRIES:
                logger.warning("Maximum retries reached, stopping reconnect attempts.")
                break
            if constants.server.WEBSOCKET_RETRY_INTERVAL:
                await asyncio.sleep(constants.server.WEBSOCKET_RETRY_INTERVAL)
            used_retries += 1
        except Exception as exc:
            logger.critical(f"Unexpected exception: {exc}")
            break

    await ConnectionManager.disconnect(ws=ws, server_id=server_id, user_id=user_id)
