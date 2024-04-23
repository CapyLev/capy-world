from config.message_transmitter import MessageTransmitter, MessageDTO
from src.modules.realm.repository import MessageRepository


class HandleIncomingWSMessagesService:
    def __init__(
        self,
        message_repository: MessageRepository,
        message_transmitter: MessageTransmitter,
    ) -> None:
        self._message_repository = message_repository
        self._message_transmitter = message_transmitter

    def execute(self, message: MessageDTO) -> None:
        pass
        # 1. must save incoming messages to storage
        # 2. send msg to transmitter
