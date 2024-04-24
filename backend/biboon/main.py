import logging.config
from typing import Any

from sanic import Sanic, SanicException
from sanic_cors import CORS

from config import constants, LOGGING_CONF, Storage
from config.message_transmitter import RabbitMQTransmitter

from src.modules import models
from src.modules.routers import api

logging.config.dictConfig(LOGGING_CONF)


def get_web_app() -> Sanic:
    try:
        application = Sanic(
            name=constants.server.NAME,
        )
    except SanicException:
        application = Sanic.get_app(
            name=constants.server.NAME,
        )

    Sanic.start_method = "forkserver"

    CORS(application, resources={r"/*": {"origins": constants.server.ORIGINS}})

    application.blueprint(blueprint=api)

    return application


app: Sanic = get_web_app()


@app.listener("before_server_start")
async def init_all(*_: Any) -> None:
    await RabbitMQTransmitter().connect()
    await Storage.initialize(models)


@app.listener("after_server_stop")
async def close_all(*_: Any) -> None:
    await RabbitMQTransmitter().disconnect()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        host=constants.server.HOST,
        port=constants.server.PORT,
        ws_max_size=constants.server.WEBSOCKET_MAX_SIZE,
        ws_max_queue=constants.server.WEBSOCKET_MAX_QUEUE,
        ws_ping_timeout=constants.server.WEBSOCKET_PING_TIMEOUT,
        ws_ping_interval=constants.server.WEBSOCKET_PING_INTERVAL,
        reload=True,
        workers=constants.server.WORKERS,
        log_config=LOGGING_CONF,
    )
