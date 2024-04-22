from datetime import datetime

from config import constants
from config.message_transmitter import MessageTransmitter
from src.modules.realm.repository import MessageRepository
from src.utils.transmitter_utils import convert_msg_document_to_transmitter_dto


class SendWelcomeMsgService:
    WELCOME_MESSAGE_TMP = "New user was joined to your server. Say hello to {username}."

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
        username: str,
    ) -> None:
        welcome_message = await self._message_repository.create_message(
            server_id=server_id,
            user_id=constants.server.ADMIN_USER_ID,
            attachments=[],
            created_at=datetime.now(),
            content=self.WELCOME_MESSAGE_TMP.format(username=username),
        )

        await self._message_repository.insert_one(welcome_message)
        # TODO: изменить роунтинг ключ на чтото понятное
        await self._message_transmitter.send(
            message=await convert_msg_document_to_transmitter_dto(welcome_message),
            routing_key='test',  # FIXME: ...
        )
