from datetime import datetime

from sanic import Websocket

from src.modules.realm.repository.message_repository import MessageRepository
from src.modules.realm.models import MessageDocument

class ConnectToServerService:
    WELCOME_MESSAGE_TMP = 'New user was joined to your server. Say hello to {username}.'

    def __init__(
        self,
        message_repository: MessageRepository,
    ) -> None:
        self._message_repository = message_repository

    async def _get_welcome_message(
        self,
        server_id: int,
        user_id: int,
    ) -> MessageDocument:
        return await self._message_repository.create_message(
            server_id=server_id,
            user_id=user_id,
            # get from userdao which will get data from iapi (core server)
            content=self.WELCOME_MESSAGE_TMP.format(username=user_id),
            attachments=[],
            created_at=datetime.now(),
        )

    async def execute(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None:
        welcome_message = await self._get_welcome_message(
            server_id=server_id,
            user_id=user_id
        )



