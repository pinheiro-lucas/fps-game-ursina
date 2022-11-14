from dotenv import dotenv_values
from websocket import WebSocket

import json


def on_error(error):
    print(error)
    exit()


class Server:
    def __init__(self):
        self.env = dotenv_values()
        self.ip = self.env.get("SERVER_IP", "localhost")
        self.port = self.env.get("SERVER_PORT", 3000)

        self.server = WebSocket()
        try:
            self.server.connect(f"ws://{self.ip}:{self.port}")
        except Exception as err:
            on_error(err)

    def send_player_info(self, player):
        try:
            self.server.send(player.to_json_str())
        except Exception as err:
            on_error(err)
    
    def send(self, payload: dict[str]):
        try:
            self.server.send(json.dumps(payload))
        except Exception as err:
            on_error(err)

    def receive(self):
        try:
            self.send({"type": "watcher"})
            return json.loads(self.server.recv())
        except Exception as err:
            on_error(err)
