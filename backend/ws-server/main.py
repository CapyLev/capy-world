import logging.config
from typing import Any

from sanic import Sanic
from sanic_cors import CORS

from sanic.request import Request
from sanic.response import JSONResponse

from config import constants, LOGGING_CONF
from config import rabbitmq_transmitter, Storage

from src.modules import models, MessageDocument
from src.modules.realm.repository import message_repository

logging.config.dictConfig(LOGGING_CONF)

app = Sanic.get_app(
    name=constants.server.NAME,
    force_create=True,
)
Sanic.start_method = "fork"

CORS(app, resources={r"/*": {"origins": constants.server.ORIGINS}})


@app.listener("before_server_start")
async def init_all(*_: Any) -> None:
    await rabbitmq_transmitter.connect()
    await Storage.initialize(models)


@app.listener("after_server_stop")
async def close_all(*_: Any) -> None:
    await rabbitmq_transmitter.disconnect()


@app.route("/")
async def test(_: Request) -> JSONResponse:
    await message_repository.insert_one(
        MessageDocument(
            server_id=1,
            user_id=1,
            content="Hello World!",
        )
    )
    return JSONResponse(body={"message": "Document inserted"})


if __name__ == "__main__":
    app.run(
        host=constants.server.HOST,
        port=constants.server.PORT,
        workers=constants.server.WORKERS,
        debug=constants.server.DEBUG,
        auto_reload=constants.server.DEBUG,
        version=constants.server.HTTP_VERSION,
        dev=constants.server.DEBUG,
        fast=True,
    )
