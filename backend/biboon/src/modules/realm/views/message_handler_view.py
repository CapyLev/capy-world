from sanic import Request, Websocket

from src.modules.realm.connection_manager import ConnectionManager
from src.modules.realm.services import HandleIncomingWSMessagesService


async def message_handler_view(
    _: Request,
    ws: Websocket,
    server_id: int,
    user_id: int,
):
    await ConnectionManager.connect(
        ws=ws,
        user_id=user_id,
        server_id=server_id,
    )

    service = HandleIncomingWSMessagesService()

    async for msg in ws:
        service.execute()
        await ws.send(msg)
