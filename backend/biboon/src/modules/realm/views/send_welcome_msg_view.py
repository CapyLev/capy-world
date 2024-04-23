from sanic import Request
from sanic.response import JSONResponse

from config import rabbitmq_transmitter
from src.modules.realm.repository import MessageRepository
from src.modules.realm.services import SendWelcomeMsgService


async def send_welcome_msg_view(request: Request) -> JSONResponse:
    data = request.json

    service = SendWelcomeMsgService(
        message_repository=MessageRepository(),
        message_transmitter=rabbitmq_transmitter,
    )
    await service.execute(server_id=data["server_id"], user_id=data["user_id"])
    return JSONResponse(status=200)
