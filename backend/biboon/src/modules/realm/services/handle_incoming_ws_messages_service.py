import logging

import ujson

from config.message_transmitter import MessageTransmitter, MessageDTO, RoutingKey
from src.modules.realm.daos import MessageDAO
from src.utils.singlton_meta import SingletonMeta

logger = logging.getLogger(__name__)


class HandleIncomingWSMessagesService(metaclass=SingletonMeta):
    def __init__(
        self,
        message_dao: MessageDAO,
        message_transmitter: MessageTransmitter,
    ) -> None:
        self._message_dao = message_dao
        self._message_transmitter = message_transmitter

    async def execute(
        self,
        message_from_connection: str,
    ) -> bool:
        if not message_from_connection:
            return False

        try:
            message_dto = MessageDTO(**ujson.loads(message_from_connection))
        except ujson.JSONDecodeError:
            logger.exception(f"Failed to decode message from {message_from_connection}")
            return True

        try:
            await self._message_dao.insert_one(message_dto=message_dto)
        except Exception as exc:
            logger.exception(f'Error inserting message: {message_from_connection}. Error: {exc}')
            return True

        try:
            await self._message_transmitter.send(
                message=message_dto,
                routing_key=RoutingKey.EVERYONE,
            )
        except Exception as exc:
            logger.exception(f'Error sending message: {message_from_connection}. Error: {exc}')
            return True
