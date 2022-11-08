import asyncio

from ursina import *
from ursina.shaders import lit_with_shadows_shader

from websocket import WebSocket
from dotenv import dotenv_values

import json
import threading

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.enemy import Enemy

if __name__ == "__main__":
    env = dotenv_values()

    DEVELOPMENT_MODE = json.loads(env['DEVELOPMENT_MODE'])
    SERVER_IP = env['SERVER_IP']
    SERVER_PORT = env['SERVER_PORT']

    nickname = input("Nickname: ").capitalize()

    server = WebSocket()
    server.connect(f"ws://{SERVER_IP}:{SERVER_PORT}")

    Entity.default_shader = lit_with_shadows_shader

    game = Ursina(
        title="Simple FPS Game",
        vsync=True,
        fullscreen=True,
        borderless=False,
        forced_aspect_ratio=False,
        show_ursina_splash=not DEVELOPMENT_MODE,
        development_mode=DEVELOPMENT_MODE,
        editor_ui_enabled=DEVELOPMENT_MODE
    )

    game.map = Map()
    player = Player((0, 0, 0), nickname)
    pos_player = player.position
    Ghook((3, 10, 3), player)

    # Todo: Player crash
    def close():
        player.online = False
        server.send(player.to_json_str())
        exit()

    # All the custom commands here
    commands = {
        "escape": close,
        "left mouse": player.shoot
    }
    server.send(player.to_json_str())

    # Multiplayer thread
    def receive():
        enemies = {}

        while True:
            # Update rate
            time.sleep(.01)
            # Receive server information
            for enemy in json.loads(server.recv()).values():
                enemy_id = enemy["id"]
                if enemy_id != nickname:
                    # Creates/updates each player position
                    if enemy_id in enemies:
                        enemies[enemy_id].world_position = enemy["pos"]
                    else:
                        e = Enemy(enemy["pos"])
                        enemies[enemy_id] = e

    multiplayer = threading.Thread(target=receive, daemon=True)
    multiplayer.start()

    # Update is better to make some features
    def update():
        global pos_player

        # Send player position every change
        if player.position != pos_player:
            server.send(player.to_json_str())
        pos_player = player.position

        # key: https://www.ursinaengine.org/cheat_sheet_dark.html#Keys
        # value: 0 or 1 (1 is pressed)
        for key, value in held_keys.items():
            if key in commands and value != 0:
                # Calls the function
                commands[key]()

    game_keys = ("left mouse down", "w", "a", "s", "d", "escape")
    def input(key):
        global game_keys

        # Send every bullet
        if key in game_keys:
            server.send(player.to_json_str())

    game.run()
