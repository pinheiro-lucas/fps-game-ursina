from dotenv import dotenv_values
from websocket import WebSocket

import websocket._exceptions as err

import json


class Server:
    def __init__(self):
        self.env = dotenv_values()
        self.ip = self.env.get("SERVER_IP", "localhost")
        self.port = self.env.get("SERVER_PORT", 3000)

        self.server = WebSocket()
        try:
            self.server.connect(f"ws://{self.ip}:{self.port}")
        except ConnectionError:
            print("Can't reach the host")

    def send_player_info(self, player):
        try:
            self.server.send(player.to_json_str())
        except err.WebSocketConnectionClosedException:
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            print("WebSocketTimeoutException")
        except:
            print("Error on sending data to server")
    
    def send(self, payload: dict[str]):
        try:
            self.server.send(json.dumps(payload))
        except err.WebSocketConnectionClosedException:
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            print("WebSocketTimeoutException")
        except:
            print("Error on sending data to server")

    def receive(self) -> dict[str] | None:
        try:
            self.send({ "type": "watcher" })
            return json.loads(self.server.recv())
        except err.WebSocketConnectionClosedException:
            # Todo: Log
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            # Todo: Log
            print("WebSocketTimeoutException")
        except:
            print("Error receiving data from server")
