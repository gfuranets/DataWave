import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: dict[int, WebSocket] = {}
        self.cmd_queues: dict[int, asyncio.Queue] = {}

    async def connect(self, ship_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[ship_id] = websocket
        self.cmd_queues[ship_id] = asyncio.Queue()

    def disconnect(self, ship_id: int):
        self.connections.pop(ship_id, None)
        self.cmd_queues.pop(ship_id, None)

    async def send_command(self, ship_id: int, command: str) -> bool:
        queue = self.cmd_queues.get(ship_id)
        if queue is None:
            return False

        while not queue.empty():
            try:
                queue.get_nowait()
            except asyncio.QueueEmpty:
                break
        await queue.put(command)
        return True
