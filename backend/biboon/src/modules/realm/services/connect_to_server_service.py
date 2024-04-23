from sanic import Websocket

from src.modules.realm.repository.message_repository import MessageRepository


class ConnectToServerService:
    def __init__(
        self,
        message_repository: MessageRepository,
    ) -> None:
        self._message_repository = message_repository

    async def execute(
        self,
        ws: Websocket,
        server_id: int,
        user_id: int,
    ) -> None:
        # in this service we can handle online status of user by keeping it in redis
        # add fetching messages from storage and return it
        pass
