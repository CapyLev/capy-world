import logging.config
from typing import Any

from sanic import Sanic
from sanic_cors import CORS
from sanic.response import json as sanic_json

from config import constants, LOGGING_CONF
from src.modules.message_transmitter import rabbitmq_transmitter
from src.modules.storage import message_storage, MessageDocument

logging.config.dictConfig(LOGGING_CONF)

app = Sanic.get_app(
    name=constants.server.NAME,
    force_create=True,
)
CORS(app, resources={r"/*": {"origins": constants.server.ORIGINS}})


@app.listener("before_server_start")
async def init_all(*_: Any) -> None:
    await rabbitmq_transmitter.connect()
    await message_storage.initialize()


@app.listener("after_server_stop")
async def close_all(*_: Any) -> None:
    await rabbitmq_transmitter.disconnect()



@app.route("/")
async def test(request):
    await message_storage.insert_one(
        MessageDocument(
            server_id=1,
            user_id=1,
            content="Hello World!",
        )
    )
    return sanic_json({"message": "Document inserted"})


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
