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
from src.modules.routers import api

logging.config.dictConfig(LOGGING_CONF)


def get_web_app() -> Sanic:
    application = Sanic(
        name=constants.server.NAME,
        log_config=LOGGING_CONF,
    )
    Sanic.start_method = "fork"

    CORS(application, resources={r"/*": {"origins": constants.server.ORIGINS}})

    application.blueprint(blueprint=api)
    return application


app: Sanic = get_web_app()


@app.listener("before_server_start")
async def init_all(*_: Any) -> None:
    await rabbitmq_transmitter.connect()
    await Storage.initialize(models)


@app.listener("after_server_stop")
async def close_all(*_: Any) -> None:
    await rabbitmq_transmitter.disconnect()


if __name__ == "__main__":
    app.run(
        host=constants.server.HOST,
        port=constants.server.PORT,
        workers=constants.server.WORKERS,
        debug=constants.server.DEBUG,
        auto_reload=False,
        version=constants.server.HTTP_VERSION,
        dev=constants.server.DEBUG,
        access_log=False,
    )
