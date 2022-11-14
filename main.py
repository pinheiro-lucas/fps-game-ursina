from ursina import *
from ursina.shaders import lit_with_shadows_shader

from threading import Thread
from random import choice

import json

from src.player import Player
from src.map import Map
from src.grappling_hook import Ghook
from src.enemy import Enemy

from config import env, server

if __name__ == "__main__":
    DEVELOPMENT_MODE = json.loads(env.get("DEVELOPMENT_MODE", "false"))
    FULLSCREEN = json.loads(env.get("FULLSCREEN", "true"))

    nickname = input("Nickname: ").capitalize()

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
    # Map respawn spots
    respawns = [
        (-18, -2.5, -1), (61, -5.5, 5), (22, 2, 58),
        (81, 2, 73), (5.5, -2.5, 75), (-23, -2.5, 70),
        (-82, 2, 75), (-82, 1, 9), (-77, -2.5, -19),
        (-27, -2.5, -22), (-31.5, -2.5, 18.5), (75, 2, -70),
        (30, -2.5, -79.5), (-29, 2.5, -78.5), (0.5, -2.5, -35.5)
    ]
    player = Player(nickname, choice(respawns))
    enemies = {}
    pos_player = player.position
    Ghook((3, 10, 3), player)

    score_text = Text("", position=(-.85, .45))

    # All the custom commands here
    commands = {
        "escape": exit,
        # "left mouse": player.shoot
    }

    # Send connection info
    server.send_info(player)

    # Multiplayer thread
    def network():
        global enemies
        while True:
            # Update rate
            time.sleep(.01)

            # Receive server information
            data = server.receive()

            for enemy in data.values():
                enemy_id = enemy["id"]
                enemy["pos"][1] += 1

                # Ignore himself
                if enemy_id != nickname:
                    # Creates/updates each player position
                    if enemy_id in enemies:
                        enemies[enemy_id].world_position = enemy["pos"]
                        enemies[enemy_id].rotation = enemy["rot"]
                    else:
                        enemies[enemy_id] = Enemy(
                            enemy["pos"],
                            enemy["rot"],
                            enemy_id,
                            enemy["color"]
                        )
                else:
                    if enemy["hp"] != player.hp:
                        if enemy["hp"] > 0:
                            player.hp = enemy["hp"]
                        else:
                            player.world_position = choice(respawns)
                            player.hp = 100

    def network_aux():
        global enemies
        while True:
            # Update rate
            time.sleep(.5)

            # Receive server information
            data = server.receive()

            for enemy_id in list(enemies):
                if enemy_id not in data.keys():
                    destroy(enemies[enemy_id])
                    del enemies[enemy_id]

            # Update score
            received_score_text = "\n".join(list(map(
                lambda x: f"{x['id']}: {x['score']}",
                data.values()
            )))

            if received_score_text != score_text.text:
                score_text.text = received_score_text

    # Check if server has sent an error
    data = server.receive()

    if "error" in data.keys():
        print(f"\nERROR: {data['error']}\n")
        exit()
    else:
        """
            System idea: 
                - Multiplayer is running in another thread
                    Why? Better performance and while True loop
                - Everything that doesn't need to update fast will run in another thread
                    Why? Better performance
        """
        # Network thread
        Thread(target=network, daemon=True).start()
        # Auxiliar thread
        Thread(target=network_aux, daemon=True).start()

    # Update is better to make some features
    def update():
        global pos_player
        # Send player position every change
        if player.position != pos_player:
            # Check if player falls from the map
            if player.world_y <= -5:
                player.world_position = choice(respawns)
            server.send_info(player)
            pos_player = player.position

        # Send player info on mouse change
        if mouse.moving:
            server.send_info(player)

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
            server.send_info(player)

    game.run()
