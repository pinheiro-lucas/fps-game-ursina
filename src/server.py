import socketio
from aiohttp import web

server = socketio.AsyncServer()
app = web.Application()

server.attach(app)


@server.event
async def connect(client_id, *args, **kwargs):
    print(f'Conectado: {client_id}')


@server.event
async def disconnect(client_id, *args, **kwargs):
    print(f'Desconectado: {client_id}')


@server.event
async def receive(client_id, data):
    print(f'[{data["name"]}] => {data["message"]}')
    await server.emit('receive', data)


if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8000)
