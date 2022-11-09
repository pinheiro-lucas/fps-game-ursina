from websocket import WebSocket

import websocket._exceptions as err

from dotenv import dotenv_values

import json
import time
import os


class Server:
    def __init__(self, player):
        self.env = dotenv_values()
        self.ip = self.env['SERVER_IP'] if os.path.isfile(".env") else "127.0.0.1"
        self.port = self.env['SERVER_PORT'] if os.path.isfile(".env") else 3000

        self.server = WebSocket()
        try:
            self.server.connect(f"ws://{self.ip}:{self.port}")
        except ConnectionError:
            print("Erro ao se conectar ao Servidor")

        self.player = player

    def send_info(self):
        try:
            self.server.send(self.player.to_json_str())
        except err.WebSocketConnectionClosedException:
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            print("WebSocketTimeoutException")
        except:
            print("Ruim send")

    def receive(self):
        try:
            return json.loads(self.server.recv()).values()
        except err.WebSocketConnectionClosedException:
            # Todo: Log
            print("WebSocketConnectionClosedException")
        except err.WebSocketTimeoutException:
            # Todo: Log
            print("WebSocketTimeoutException")
        except:
            print("Ruim receive")

    def close(self):
        self.player.online = False
        self.send_info()
        exit()

    def send_ping(self):
        while True:
            try:
                self.server.ping(self.player.nickname)
                time.sleep(.5)
            except:
                self.close()
