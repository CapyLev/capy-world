from datetime import datetime

from sanic import Request
from sanic.response import JSONResponse

from config.message_transmitter import RabbitMQTransmitter, RoutingKey, MessageDTO
from src.modules.realm.daos import MessageDAO


async def ping_view(_: Request) -> JSONResponse:
    return JSONResponse({"message": "Hello World!"})

msg = MessageDTO(
    server_id=1,
    user_id=1,
    content="Hello World!",
    attachments=[],
    created_at=datetime.now().isoformat()
)


async def test_mongo_view(_: Request) -> JSONResponse:
    message_dao = MessageDAO()
    await message_dao.insert_one(
        message_dto=msg
    )
    return JSONResponse(body={"message": "Document inserted"})


async def test_rabbit_view(_: Request) -> JSONResponse:
    await RabbitMQTransmitter().send(
        message=msg,
        routing_key=RoutingKey.EVERYONE,
    )
    return JSONResponse(body={"message": "msg sended"})
