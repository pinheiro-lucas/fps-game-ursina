from ursina import *
from ursina.shaders import lit_with_shadows_shader

from threading import Thread
from random import choice

import json

from src.player import Player, Bullet
from src.map import Map
from src.grappling_hook import Ghook
from src.enemy import Enemy
from src.multiplayer import Multiplayer

from config import env, server, respawns, hooks

if __name__ == "__main__":
    DEVELOPMENT_MODE = json.loads(env.get("DEVELOPMENT_MODE", "false"))
    FULLSCREEN = json.loads(env.get("FULLSCREEN", "true"))

    # Prevents any error if user closes the game
    try:
        nickname = input("Nickname: ").capitalize()
    except KeyboardInterrupt:
        print("\nConnection closed by the user")
        exit()

    Entity.default_shader = lit_with_shadows_shader

    game = Ursina(
        title="Multiplayer FPS",
        vsync=False,
        fullscreen=FULLSCREEN,
        borderless=False,
        forced_aspect_ratio=False,
        show_ursina_splash=not DEVELOPMENT_MODE,
        development_mode=DEVELOPMENT_MODE,
        editor_ui_enabled=DEVELOPMENT_MODE,
        fps_counter=True
    )

    game.map = Map()
    player = Player(nickname, choice(respawns))
    pos_player = player.position
    Ghook(hooks, player)
    multiplayer = Multiplayer(player, nickname)

    # All the custom commands here
    commands = {
        "escape": exit,
        # "left mouse": player.shoot
    }

    # Send connection info
    server.send_player_info(player)

    # Check if server has sent an error
    try:
        server_data = server.receive()
        if "error" in server_data.keys():
            print(f"\nERROR: {server_data['error']}\n")
            exit()
    except Exception as server_error:
        print(server_error)
        exit()

    """
        System idea: 
            - Multiplayer is running in another thread
                Why? Better performance and while True loop
            - Everything that doesn't need to update fast will run in another thread
                Why? Better performance
    """
    # Network thread
    Thread(target=multiplayer.network, daemon=True).start()
    # Auxiliar thread
    Thread(target=multiplayer.network_aux, daemon=True).start()
    # Bullets thread
    # Thread(target=multiplayer.network_bullet, daemon=True).start()

    # Update is better to make some features
    def update():
        global pos_player
        # Send player position every change
        if player.position != pos_player:
            # Check if player falls from the map
            if player.world_y <= -5:
                player.world_position = choice(respawns)
            server.send_player_info(player)
            pos_player = player.position

        # Send player info on mouse change
        if mouse.moving:
            server.send_player_info(player)

        # key: https://www.ursinaengine.org/cheat_sheet_dark.html#Keys
        # value: 0 or 1 (1 is pressed)
        for key, value in held_keys.items():
            if key in commands and value != 0:
                # Calls the function
                commands[key]()

    def input(key):
        # Send every bullet
        if key == "left mouse down":
            player.shoot()
            server.send_player_info(player)

    game.run()
