import logging
from dataclasses import dataclass

import ujson

from aio_pika import connect_robust, Message, ExchangeType
from aio_pika.abc import (
    AbstractRobustConnection,
    AbstractRobustChannel,
    AbstractExchange,
    AbstractQueue,
)

from config.constants import constants
from .interfaces import MessageTransmitter, MessageDTO


@dataclass
class RabbitMQTransmitter(MessageTransmitter):
    class RabbitMQClientError(Exception):
        pass

    class NotConnectedToRabbitMQError(RabbitMQClientError):
        pass

    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None
    exchange: AbstractExchange | None = None
    queue: AbstractQueue | None = None

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
        self.exchange = None
        self.queue = None

    async def connect(self) -> None:
        try:
            self.connection = await connect_robust(constants.rabbitmq.RABBITMQ_URL)
            self.channel = await self.connection.channel(publisher_confirms=False)

            self.exchange = await self.channel.declare_exchange(
                name=constants.rabbitmq.RABBITMQ_MSG_EXCHANGE_NAME,
                type=ExchangeType.FANOUT,
            )

            self.queue = await self.channel.declare_queue(
                constants.rabbitmq.RABBITMQ_MSG_QUEUE_NAME, durable=True
            )

            await self.queue.bind(self.exchange)
            await self.queue.consume(self._notify, no_ack=True)

            logging.info("Rabbitmq successfully connected.")
        except Exception as e:
            logging.error(msg=str(e), extra=e.__dict__)
            await self._clear()

    async def disconnect(self) -> None:
        await self._clear()

    # TODO: добавить какой-то мб енам для того чтобы определять куда отправлять сообщение в принципе
    # тк роутинг по ключу не самый удобный вариант
    async def send(
        self,
        message: MessageDTO,
        routing_key: str,
    ) -> None:
        if not self.channel:
            raise self.NotConnectedToRabbitMQError

        async with self.channel.transaction():
            message = Message(
                body=ujson.dumps(message.model_dump()).encode(),
                headers={"content_type": "application/json"},
            )

            await self.exchange.publish(
                message,
                routing_key=routing_key,
            )

    async def _notify(self, m):
        logging.info(m.body)


rabbitmq_transmitter: RabbitMQTransmitter = RabbitMQTransmitter()
