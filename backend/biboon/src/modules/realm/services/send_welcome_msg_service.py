from datetime import datetime

from config import constants
from config.message_transmitter import MessageTransmitter, RoutingKey, MessageDTO
from src.modules.realm.repository import MessageRepository


class SendWelcomeMsgService:
    WELCOME_MESSAGE_TMP = "New user was joined to your server. Say hello to {user_id}."

    def __init__(
        self,
        message_repository: MessageRepository,
        message_transmitter: MessageTransmitter,
    ) -> None:
        self._message_repository = message_repository
        self._message_transmitter = message_transmitter

    async def execute(
        self,
        server_id: int,
        user_id: int,
    ) -> None:
        message = MessageDTO(
            server_id=server_id,
            user_id=constants.server.ADMIN_USER_ID,
            attachments=[],
            created_at=datetime.now().isoformat(),
            content=self.WELCOME_MESSAGE_TMP.format(user_id=user_id),
        )
        await self._message_repository.insert_one(
            message_dto=message,
        )

        await self._message_transmitter.send(
            message=message,
            routing_key=RoutingKey.EVERYONE,
        )
