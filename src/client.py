from dotenv import dotenv_values
from websocket import WebSocket

import websocket._exceptions as err

import json


class Server:
    def __init__(self, player):
        self.env = dotenv_values()
        self.ip = self.env.get("SERVER_IP", "localhost")
        self.port = self.env.get("SERVER_PORT", 3000)

        self.server = WebSocket()
        try:
            self.server.connect(f"ws://{self.ip}:{self.port}")
        except ConnectionError:
            print("Can't reach the host")

        self.player = player

    def send_info(self):
        try:
            self.server.send(self.player.to_json_str())
        except err.WebSocketConnectionClosedException:
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            print("WebSocketTimeoutException")
        except:
            print("Error on sending data to server")

    def receive(self) -> dict[str] | None:
        try:
            return json.loads(self.server.recv())
        except err.WebSocketConnectionClosedException:
            # Todo: Log
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            # Todo: Log
            print("WebSocketTimeoutException")
        except:
            print("Error receiving data from server")

    def close(self):
        self.player.online = False
        self.send_info()
        exit()
