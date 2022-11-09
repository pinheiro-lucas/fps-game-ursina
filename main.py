from ursina import *
from ursina.shaders import lit_with_shadows_shader

from dotenv import dotenv_values

from threading import Thread
import json
import os

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.client import Server
from src.enemy import Enemy

if __name__ == "__main__":
    env = dotenv_values()
    DEVELOPMENT_MODE = json.loads(env['DEVELOPMENT_MODE']) if os.path.isfile(".env") else False

    nickname = input("Nickname: ").capitalize()

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
    server = Server(player)

    # All the custom commands here
    commands = {
        "escape": server.close,
        "left mouse": player.shoot
    }
    # Send connection info
    server.send_info()

    # Multiplayer thread
    def network():
        enemies = {}

        while True:
            # Update rate
            time.sleep(.01)
            # Receive server information
            teste = server.receive()
            for enemy in teste:
                enemy_id = enemy["id"]
                if enemy_id != nickname:
                    # Creates/updates each player position
                    if enemy_id in enemies:
                        enemies[enemy_id].world_position = enemy["pos"]
                    else:
                        e = Enemy(enemy["pos"])
                        enemies[enemy_id] = e


    multiplayer = Thread(target=network, daemon=True).start()
    ping = Thread(target=server.send_ping, daemon=True).start()

    # Update is better to make some features
    def update():
        global pos_player
        # Send player position every change
        if player.position != pos_player:
            server.send_info()
        pos_player = player.position

        # key: https://www.ursinaengine.org/cheat_sheet_dark.html#Keys
        # value: 0 or 1 (1 is pressed)
        for key, value in held_keys.items():
            if key in commands and value != 0:
                # Calls the function
                commands[key]()

    def input(key):
        # Send every bullet
        if key in ("left mouse down",):
            server.send_info()

    game.run()
