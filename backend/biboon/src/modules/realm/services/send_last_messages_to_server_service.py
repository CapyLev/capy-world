from config.message_transmitter import MessageDTO
from src.modules.realm.models import MessageDocument
from src.modules.realm.daos.message_dao import MessageDAO
from src.utils.singlton_meta import SingletonMeta


class SendLastMessagesToServerService(metaclass=SingletonMeta):
    DEFAULT_LAST_SERVER_MESSAGES_CHUNK_SIZE = 200

    def __init__(
        self,
        message_dao: MessageDAO,
    ) -> None:
        self._message_dao = message_dao

    async def _convert_to_message_dto(
        self,
        models: list[MessageDocument],
    ) -> list[MessageDTO]:
        return [
            MessageDTO(
                server_id=msg.server_id,
                user_id=msg.user_id,
                content=msg.content,
                attachments=msg.attachments,
                created_at=msg.created_at,
            )
            for msg in models
        ]

    async def execute(
        self,
        server_id: int,
    ) -> list[MessageDTO]:
        last_chunk_of_server_messages = (
            await self._message_dao.fetch_last_server_messages(
                server_id=server_id,
                chunk_size=self.DEFAULT_LAST_SERVER_MESSAGES_CHUNK_SIZE,
            )
        )

        converted_messages = await self._convert_to_message_dto(last_chunk_of_server_messages)
        return list(reversed(converted_messages))