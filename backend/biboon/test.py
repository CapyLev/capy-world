import json
import asyncio
from datetime import datetime
import websockets


async def send_message():
    uri = "ws://localhost:6967/api/realm/ws/message_handler/1/1"
    async with websockets.connect(uri) as ws:
        for i in range(22):
            print(f'Sending message {i}')
            message = json.dumps({
                "server_id": 1,
                "user_id": 1,
                "content": f"message {i}",
                "attachments": [],
                "created_at": datetime.now().isoformat()
            })
            await ws.send(message)


async def main():
    await send_message()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
