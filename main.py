from ursina import *
from ursina.shaders import lit_with_shadows_shader

from websocket import WebSocket
import json

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.enemy import Enemy

if __name__ == "__main__":
    DEVELOPMENT_MODE = True

    nickname = input("Nickname: ").capitalize()

    server = WebSocket()
    server.connect("ws://localhost:3000")

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
    Ghook((3, 10, 3), player)
    enemies = {}

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

    # Update is better to make some features
    def update():
        server.send(player.to_json_str())
        for enemy in json.loads(server.recv()).values():
            enemy_id = enemy["id"]
            if enemy_id != nickname:
                if enemy_id not in enemies.keys():
                    e = Enemy(enemy["pos"])
                    enemies[enemy_id] = e

                enemies[enemy_id].world_position = enemy["pos"]
        # key: https://www.ursinaengine.org/cheat_sheet_dark.html#Keys
        # value: 0 or 1 (1 is pressed)
        for key, value in held_keys.items():
            if key in commands and value != 0:
                # Calls the function
                commands[key]()

    game.run()
