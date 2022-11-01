import socketio
import asyncio
from aioconsole import ainput, aprint

client = socketio.AsyncClient()
name = ''


@client.event
async def connect():
    print('Cliente conectado')


@client.event
async def disconnect():
    print('Cliente desconectado')


@client.event
async def receive(data):
    if data['name'] != name:
        print(f'[{data["name"]}] => {data["message"]}')


async def send():
    global name
    name = input('Nome: ')
    while True:
        await asyncio.sleep(.1)
        message = await ainput()
        await client.emit('receive', {
            'name': name,
            'message': message
        })


async def connect_to_server(ip: str):
    await client.connect(ip)
    await client.wait()


async def main():
    await asyncio.gather(
        connect_to_server('http://localhost:8000'),
        send()
    )

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
