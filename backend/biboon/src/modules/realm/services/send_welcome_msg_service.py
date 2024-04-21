from datetime import datetime

from src.modules.realm.repository import MessageRepository

from config import constants


class SendWelcomeMsgService:
    WELCOME_MESSAGE_TMP = "New user was joined to your server. Say hello to {username}."

    def __init__(
        self,
        message_repository: MessageRepository,
    ) -> None:
        self._message_repository = message_repository

    def execute(
        self,
        server_id: int,
        username: str,
    ) -> None:
        self._message_repository.create_message(
            server_id=server_id,
            user_id=constants.server.ADMIN_USER_ID,
            attachments=[],
            created_at=datetime.now(),
            content=self.WELCOME_MESSAGE_TMP.format(username=username),
        )
