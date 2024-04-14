from fastapi import APIRouter, WebSocket


server_router = APIRouter()


@server_router("/ws/server")
async def ws_entrypoint_chat(websocket: WebSocket) -> None:
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received message from client: {data}")
            for client in connected_clients:
                if client != websocket:
                    await client.send_text(f"Message from server: {data}")
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        connected_clients.remove(websocket)
