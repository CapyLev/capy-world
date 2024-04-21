from datetime import datetime
from uuid import UUID, uuid4

from beanie import Document
from pydantic import Field
import pymongo


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
