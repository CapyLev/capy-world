from datetime import datetime

import pymongo

from ..models import MessageDocument


class MessageRepository:
    DEFAULT_MESSAGE_CHUNK_SIZE = 200

    async def insert_many(self, messages: list[MessageDocument]):
        await MessageDocument.insert_many(messages)

    async def insert_one(self, message: MessageDocument):
        await MessageDocument.insert_one(message)

    async def fetch_last_server_messages(
        self,
        server_id: int,
        chunk_size: int = DEFAULT_MESSAGE_CHUNK_SIZE,
    ) -> list[MessageDocument]:
        messages = await MessageDocument.find(
            MessageDocument.server_id == server_id,
            sort=pymongo.DESCENDING,
            ).to_list(length=chunk_size)

        return messages

    async def create_message(
        self,
        server_id: int,
        user_id: int,
        content: str,
        attachments: list[str | None],
        created_at: datetime,
    ) -> MessageDocument:
        return MessageDocument(
            server_id=server_id,
            user_id=user_id,
            content=content,
            attachments=attachments,
            created_at=created_at.isoformat(),
        )


message_repository: MessageRepository = MessageRepository()
