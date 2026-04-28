from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def send_command(self, command: str, websocket: WebSocket):
        await websocket.send_text(command)

    async def receive_data(self, websocket: WebSocket):
        received = await websocket.receive_text()
        received_processed = received.split(",")
        return received_processed[:1], received_processed[1:]
