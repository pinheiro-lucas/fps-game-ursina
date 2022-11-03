import socketio
from aiohttp import web

HOST = "0.0.0.0"
PORT = 8000
PLAYERS, MAX_PLAYERS = dict(), 1


server = socketio.AsyncServer()
app = web.Application()

server.attach(app)


@server.event
async def connect(player_id, *args, **kwargs):
    if len(PLAYERS) < MAX_PLAYERS:
        PLAYERS[player_id] = dict()
        print(f'Connected: {player_id}')
    else:
        # Todo: Disconnects the player
        print(f"Server is full!")


@server.event
async def disconnect(player_id, *args, **kwargs):
    del PLAYERS[player_id]
    print(f'Disconnected: {player_id}')


@server.event
async def receive(player_id, data):
    print(f'[{player_id}] => {data}')
    await server.emit('receive', data)


if __name__ == '__main__':
    print(f"Starting the server...")
    web.run_app(app=app, host=HOST, port=PORT)
