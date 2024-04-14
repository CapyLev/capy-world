import logging.config
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.modules.rabbitmq import rabbitmq_connection, RBMQMessageDTO
from config import constants, LOGGING_CONF

logging.config.dictConfig(LOGGING_CONF)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbitmq_connection.connect()
    yield
    await rabbitmq_connection.disconnect()


def get_server_app() -> FastAPI:
    app = FastAPI(
        title=constants.server.NAME,
        version=constants.server.VERSION,
        debug=constants.server.DEBUG,
        lifespan=lifespan,
        **constants.server.fastapi_kwargs
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=constants.server.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


app: FastAPI = get_server_app()


@app.get('/')
async def test(content: str | None = 'Test message') -> None:
    await rabbitmq_connection.send_messages(
        RBMQMessageDTO(
            content=content,
            server_id=123,
            user_id=1,
        ),
        routing_key='test',
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=constants.server.HOST,
        port=constants.server.PORT,
        workers=constants.server.WORKERS,
        log_level=constants.server.LOG_LEVEL,
        use_colors=True,
    )
