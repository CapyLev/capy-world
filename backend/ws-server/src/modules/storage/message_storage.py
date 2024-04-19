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
            pymongo.IndexModel(keys=[("server_id", 1), ("user_id", 1), ("id", 1)]),
        ]


class MessageStorage:
    DEFAULT_MESSAGE_CHUNK_SIZE = 200

    async def initialize(self):
        client = AsyncIOMotorClient(constants.mongodb.MONGO_URL)
        await beanie.init_beanie(
            database=client[constants.mongodb.MONGO_NAME],
            document_models=[MessageDocument],
        )

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


message_storage: MessageStorage = MessageStorage()
