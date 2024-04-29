from sanic import Websocket

from src.modules.realm.daos.message_dao import MessageDAO
from src.utils.singlton_meta import SingletonMeta


class ConnectToServerService(metaclass=SingletonMeta):
    DEFAULT_LAST_SERVER_MESSAGES_CHUNK_SIZE = 200

    def __init__(
        self,
        message_dao: MessageDAO,
    ) -> None:
        self._message_dao = message_dao

    async def execute(
        self,
        server_id: int,
    ) -> None:
        last_chunk_of_server_messages = await self._message_dao.fetch_last_server_messages(
            server_id=server_id,
            chunk_size=self.DEFAULT_LAST_SERVER_MESSAGES_CHUNK_SIZE,
        )

        print(last_chunk_of_server_messages)
        print(len(last_chunk_of_server_messages))
        print(type(last_chunk_of_server_messages))

