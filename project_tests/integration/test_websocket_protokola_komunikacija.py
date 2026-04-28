import unittest

from tests.helpers import APP_DIR
from manager import ConnectionManager


class FakeWebSocket:
    def __init__(self, received_text):
        self.received_text = received_text
        self.accepted = False
        self.sent_text = None

    async def accept(self):
        self.accepted = True

    async def send_text(self, text):
        self.sent_text = text

    async def receive_text(self):
        return self.received_text


class WebSocketProtokolaKomunikacijaTests(unittest.IsolatedAsyncioTestCase):
    async def test_websocket_manager_connect_send_receive_disconnect(self):
        manager = ConnectionManager()
        websocket = FakeWebSocket("1,temp=20,humidity=55")

        await manager.connect(websocket)
        await manager.send_command("a", websocket)
        ship_id, sensor_data = await manager.receive_data(websocket)
        await manager.disconnect(websocket)

        self.assertTrue(websocket.accepted)
        self.assertEqual(websocket.sent_text, "a")
        self.assertEqual(ship_id, ["1"])
        self.assertEqual(sensor_data, ["temp=20", "humidity=55"])
        self.assertEqual(manager.active_connections, [])


if __name__ == "__main__":
    unittest.main()
