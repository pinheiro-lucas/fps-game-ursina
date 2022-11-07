import time

import socketio
import asyncio
from aioconsole import ainput, aprint

HOST = "127.0.0.1"
PORT = 8000


class Server:
    def __init__(self):
        self.client = socketio.AsyncClient()
        self._player = {
            "nickname": "",
            "hp": 0
        }

        # Client events
        self.connect = self.client.event(self.connect)
        self.disconnect = self.client.event(self.disconnect)
        self.receive = self.client.event(self.receive)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, info):
        self._player = info

    async def connect(self):
        print('Connected to the server')
        # Todo: Closes main menu

    async def disconnect(self):
        print('Disconnected from the server')
        # Todo: Returns to main menu

    async def receive(self, data):
        # if data["nickname"] != self._player['nickname']:
        print(data)

    async def send(self):
        while True:
            await asyncio.sleep(.1)
            await self.client.emit('receive', self._player)

    async def connect_to_server(self, ip):
        await self.client.connect(ip)
        await self.client.wait()

    async def main(self):
        while True:
            try:
                await asyncio.gather(
                    self.connect_to_server(f"http://{HOST}:{PORT}"),
                    self.send()
                )
            except socketio.exceptions.ConnectionError:
                print("Connection failed. \nRetrying in 5s...")
            time.sleep(5)
