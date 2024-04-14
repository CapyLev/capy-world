from fastapi import WebSocket
from datetime import datetime
from typing import List

from src.modules.rabbitmq import RabbitMQClient, RBMQMessageDTO


class ConnectionManager:
    def __init__(self, rabbitmq_connection: RabbitMQClient):
        self.active_connections: List[WebSocket] = []
        self.rabbitmq_connection = rabbitmq_connection

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def handle_rabbitmq_message(self, message: RBMQMessageDTO):
        # Здесь можно добавить логику сохранения сообщения в сторейдж
        # Это место для вашей логики работы с сохранением данных

        # Отправляем сообщение на все вебсокет-соединения
        for connection in self.active_connections:
            await connection.send_text(message.content)

    async def receive_rabbitmq_messages(self):
        while True:
            try:
                # Получаем сообщения из RabbitMQ
                message = await self.rabbitmq_connection.consume_messages()
                # Обрабатываем сообщение
                await self.handle_rabbitmq_message(message)
            except Exception as e:
                # Обработка ошибок при получении сообщений из RabbitMQ
                print(f"Error receiving RabbitMQ message: {e}")

    async def start_receive_tasks(self):
        # Запускаем асинхронные задачи для получения сообщений из RabbitMQ
        await self.receive_rabbitmq_messages()

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
