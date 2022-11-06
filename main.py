from ursina import *
from ursina.shaders import lit_with_shadows_shader

import asyncio
import threading

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.client import Server

if __name__ == "__main__":
    DEVELOPMENT_MODE = True

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
    player = Player((0, 0, 0))
    grapple = Ghook((3, 10, 3), player)
    server = Server()

    # All the custom commands here
    commands = {
        "escape": exit,
        "left mouse": player.shoot
    }

    # Update is better to make some features
    def update():
        server.player = {
            "nickname": player.nickname,
            "hp": player.hp
        }
        # key: https://www.ursinaengine.org/cheat_sheet_dark.html#Keys
        # value: 0 or 1 (1 is pressed)
        for key, value in held_keys.items():
            if key in commands and value != 0:
                # Calls the function
                commands[key]()

    # Server connection stuff
    def connect():
        asyncio.run(server.main())

    connection = threading.Thread(target=connect, daemon=True)
    connection.start()

    game.run()
