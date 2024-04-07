from datetime import datetime

import ujson
import logging
from dataclasses import dataclass

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

from .constants import constants


@dataclass(frozen=True, slots=True)
class MessageDTO:
    content: str
    server_id: int
    user_id: int
    created_at: datetime = datetime.now()


@dataclass
class RabbitMQClient:
    class NotConnectedToRabbitMQError(Exception):
        pass

    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def status(self) -> bool:
        if self.connection.is_closed or self.channel.is_closed:
            return False
        return True

    async def _clear(self) -> None:
        if not self.channel.is_closed:
            await self.channel.close()
        if not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        try:
            self.connection = await connect_robust(constants.rabbitmq.RABBITMQ_URL)
            self.channel = await self.connection.channel(publisher_confirms=False)
            logging.info("Rabbitmq successfully connected.")
        except Exception as e:
            await self._clear()
            logging.error(e.__dict__)

    async def disconnect(self) -> None:
        await self._clear()

    async def send_messages(
        self,
        messages: list[MessageDTO] | MessageDTO,
        routing_key: str
    ) -> None:
        if not self.channel:
            raise self.NotConnectedToRabbitMQError

        if isinstance(messages, dict):
            messages = [messages]

        async with self.channel.transaction():
            for message in messages:
                message = Message(
                    body=ujson.dumps(message).encode()
                )

                await self.channel.default_exchange.publish(
                    message,
                    routing_key=routing_key,
                )


rabbitmq_connection: RabbitMQClient = RabbitMQClient()
