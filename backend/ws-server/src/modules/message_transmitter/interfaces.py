from abc import ABC, abstractmethod
from datetime import datetime

from pydantic import BaseModel


class MessageDTO(BaseModel):
    server_id: int
    user_id: int
    content: str
    attachments: list[str | None] = []
    created_at: str = datetime.now().isoformat()


class MessageTransmitter(ABC):
    @abstractmethod
    def status(self) -> bool:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def send(
        self,
        message: MessageDTO,
        routing_key: str,
    ) -> None:
        pass