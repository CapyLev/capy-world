import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from config import RabbitMQClient, constants


logging.basicConfig(
    level=constants.server.LOG_LEVEL,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("logs/fastapi.log"),
        logging.StreamHandler()
    ]
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()


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


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await conn_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Do something with received data if needed
    except Exception as e:
        print(f"WebSocket connection closed with exception: {e}")
    finally:
        conn_manager.disconnect(websocket)
