from config.message_transmitter import MessageTransmitter, MessageDTO, RoutingKey
from src.modules.realm.repository import MessageRepository
from src.utils.singlton_meta import SingletonMeta


class HandleIncomingWSMessagesService(metaclass=SingletonMeta):
    def __init__(
        self,
        message_repository: MessageRepository,
        message_transmitter: MessageTransmitter,
    ) -> None:
        self._message_repository = message_repository
        self._message_transmitter = message_transmitter

    async def execute(self, message_dto: MessageDTO) -> None:
        await self._message_repository.insert_one(message_dto=message_dto)
        await self._message_transmitter.send(
            message=message_dto,
            routing_key=RoutingKey.EVERYONE,
        )
