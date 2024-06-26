from typing import TypedDict, Unpack

import pymongo

from config.message_transmitter import MessageDTO
from src.utils.singlton_meta import SingletonMeta
from ..models import MessageDocument


class MessageDAO(metaclass=SingletonMeta):
    DEFAULT_MESSAGE_CHUNK_SIZE = 200

    class MessageDAOError(Exception):
        pass

    class NotEnoughDataToInsertMessageError(MessageDAOError):
        pass

    class MessageKwargsTyping(TypedDict):
        server_id: int
        user_id: int
        content: str
        attachments: list[str | None]
        created_at: str

    async def insert_many(
        self,
        messages_dto: list[MessageDTO],
    ):
        message_documents = [
            await self._create_message_document(
                server_id=message_dto.server_id,
                user_id=message_dto.user_id,
                content=message_dto.content,
                attachments=message_dto.attachments,
                created_at=message_dto.created_at,
            )
            for message_dto in messages_dto
        ]
        await MessageDocument.insert_many(message_documents)

    async def insert_one(
        self,
        message_dto: MessageDTO | None = None,
        **kwargs: Unpack[MessageKwargsTyping] | None,
    ) -> None:
        if not message_dto and not kwargs:
            raise self.NotEnoughDataToInsertMessageError

        message_document = await self._create_message_document(
            server_id=message_dto.server_id or kwargs["server_id"],
            user_id=message_dto.user_id or kwargs["user_id"],
            content=message_dto.content or kwargs["content"],
            attachments=message_dto.attachments or kwargs.get("attachments") or [],
            created_at=message_dto.created_at or kwargs["created_at"],
        )

        await MessageDocument.insert_one(message_document)

    async def fetch_last_server_messages(
        self,
        server_id: int,
        chunk_size: int = DEFAULT_MESSAGE_CHUNK_SIZE,
    ) -> list[MessageDocument]:
        return (
            await MessageDocument.find(
                {"server_id": server_id},
            )
            .sort([(MessageDocument.created_at, pymongo.DESCENDING)])
            .to_list(length=chunk_size)
        )

    async def _create_message_document(
        self,
        server_id: int,
        user_id: int,
        content: str,
        attachments: list[str | None],
        created_at: str,
    ) -> MessageDocument:
        return MessageDocument(
            server_id=server_id,
            user_id=user_id,
            content=content,
            attachments=attachments,
            created_at=created_at,
        )
