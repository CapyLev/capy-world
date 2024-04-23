from sanic import Request
from sanic.response import JSONResponse

from src.modules import MessageDocument
from src.modules.realm.repository import MessageRepository


async def ping_view(_: Request) -> JSONResponse:
    return JSONResponse({"message": "Hello World!"})


async def test_view(_: Request) -> JSONResponse:
    message_repository = MessageRepository()
    await message_repository.insert_one(
        MessageDocument(
            server_id=1,
            user_id=1,
            content="Hello World!",
        )
    )
    return JSONResponse(body={"message": "Document inserted"})
