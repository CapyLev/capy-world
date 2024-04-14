from datetime import datetime
from uuid import UUID, uuid4

import beanie
from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import Field
import pymongo

from config import constants


class MessageDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    server_id: int
    user_id: int
    content: str
    attachments: list[str | None] = Field(default_factory=list)
    created_at: str = datetime.now().isoformat()

    class Settings:
        indexes = [
            pymongo.IndexModel(keys=[("server_id", 1), ("created_at", -1)]),
            pymongo.IndexModel(keys=[("server_id", 1), ("user_id", 1)]),
        ]


class MessageStorage:
    async def initialize(self):
        client = AsyncIOMotorClient(constants.mongodb.MONGO_URL)
        await beanie.init_beanie(
            database=client[constants.mongodb.NAME],
            document_models=[MessageDocument]
        )

    async def insert_many(self, messages: list[MessageDocument]):
        [await message.insert() for message in messages]

    async def insert(self, message: MessageDocument):
        await self.insert_many([message,])

    async def fetch_last_server_messages(self, server_id: int, chunk_size: int) -> list[MessageDocument]:
        messages = (
            await MessageDocument.find(
                MessageDocument.server_id == server_id,
                sort=pymongo.DESCENDING
            ).to_list(
                length=chunk_size
            )
        )

        return messages


message_storage: MessageStorage = MessageStorage()
