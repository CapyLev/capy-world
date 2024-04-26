
import json
import asyncio
from datetime import datetime
import websockets


async def send_message(uri):
    async with websockets.connect(uri) as ws:
        while True:
            message = json.dumps({
                "server_id": 1,
                "user_id": 1,
                "content": "Test message",
                "attachments": [],
                "created_at": datetime.now().isoformat()
            })
            print(f'Sending message: {message}')
            await ws.send(message)


async def receive_messages(uri):
    async with websockets.connect(uri) as ws:
        while True:
            message = await ws.recv()
            print(f'Received message: {message}')


async def main():
    uri = "ws://localhost:6967/api/realm/ws/message_handler/1/1"
    tasks = [send_message(uri), receive_messages(uri)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
