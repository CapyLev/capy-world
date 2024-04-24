import enum
from datetime import datetime

from pydantic import BaseModel, Field


class MessageDTO(BaseModel):
    server_id: int
    user_id: int
    content: str
    attachments: list[str | None] = Field(default_factory=list)
    created_at: str = datetime.now().isoformat()


class RoutingKey(enum.StrEnum):
    EVERYONE = "message_queue"


class MessageTransmitter:
    def status(self) -> bool:
       raise NotImplementedError

    async def connect(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    async def send(
        self,
        message: MessageDTO,
        routing_key: RoutingKey,
    ) -> None:
        raise NotImplementedError
