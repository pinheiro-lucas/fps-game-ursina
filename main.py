from ursina import *
from ursina.shaders import lit_with_shadows_shader

from dotenv import dotenv_values
from threading import Thread

import json

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.client import Server
from src.enemy import Enemy

if __name__ == "__main__":
    env = dotenv_values()

    DEVELOPMENT_MODE = json.loads(env.get("DEVELOPMENT_MODE", "false"))
    FULLSCREEN = json.loads(env.get("FULLSCREEN", "true"))

    nickname = input("Nickname: ").capitalize()

    Entity.default_shader = lit_with_shadows_shader

    game = Ursina(
        title="Multiplayer FPS",
        vsync=True,
        fullscreen=FULLSCREEN,
        borderless=False,
        forced_aspect_ratio=False,
        show_ursina_splash=not DEVELOPMENT_MODE,
        development_mode=DEVELOPMENT_MODE,
        editor_ui_enabled=DEVELOPMENT_MODE,
        fps_counter=True
    )

    game.map = Map()
    # Map respawn spots
    respawns = ((0, 0, 0), (1, 0, 1), (2, 0, 2), (3, 0, 3), (4, 0, 4),
                (-1, 0, -1), (-2, 0, -2), (-3, 0, -3), (-4, 0, -4))
    player = Player((0, -100, 0), nickname)
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
            data = server.receive()

            for enemy in data.values():
                enemy_id = enemy["id"]
                enemy["pos"][1] += 1
                if enemy_id != nickname:
                    # Creates/updates each player position
                    if enemy_id in enemies:
                        enemies[enemy_id].world_position = enemy["pos"]
                        enemies[enemy_id].rotation = enemy["rot"]
                    else:
                        enemies[enemy_id] = Enemy(enemy["pos"], enemy["rot"], enemy_id, enemy["color"])

            for enemy_id in list(enemies):
                if enemy_id not in data.keys():
                    destroy(enemies[enemy_id])
                    del enemies[enemy_id]

    multiplayer = Thread(target=network, daemon=True).start()

    # First respawn spot
    data = server.receive()
    player.world_position = respawns[list(data).index(nickname)]

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
