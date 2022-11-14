from ursina import *

from config import server, respawns

from src.bullet import Bullet
from src.enemy import Enemy

from time import sleep
from random import choice


class Multiplayer:
    def __init__(self, player, nickname):
        self.enemies = {}
        self.score_text = Text("", position=(-.85, .45))
        self.player = player
        self.nickname = nickname

    # Main thread
    def network(self):
        while True:
            # Update rate
            sleep(.01)

            # Receive server information
            data = server.receive()

            for enemy in data.values():
                enemy_id = enemy["id"]
                enemy["pos"][1] += 1

                # Ignore himself
                if enemy_id != self.nickname:
                    # Creates/updates each player position
                    if enemy_id in self.enemies:
                        self.enemies[enemy_id].world_position = enemy["pos"]
                        self.enemies[enemy_id].rotation = enemy["rot"]

                        if "bullet" in enemy.keys():
                            Bullet(
                                player=enemy,
                                position=tuple(enemy["bullet"]["pos"]),
                                rotation=tuple(enemy["bullet"]["rot"]),
                                ignore_collision=True
                            )
                    else:
                        self.enemies[enemy_id] = Enemy(
                            enemy["pos"],
                            enemy["rot"],
                            enemy_id,
                            enemy["color"]
                        )
                else:
                    if enemy["hp"] != self.player.hp:
                        if enemy["hp"] > 0:
                            self.player.hp = enemy["hp"]
                        else:
                            self.player.world_position = choice(respawns)
                            self.player.hp = 100

    # Auxiliar thread
    def network_aux(self):
        while True:
            # Update rate
            sleep(.5)

            # Receive server information
            data = server.receive()

            for enemy_id in list(self.enemies):
                if enemy_id not in data.keys():
                    destroy(self.enemies[enemy_id])
                    del self.enemies[enemy_id]

            # Update score
            received_score_text = "\n".join(list(map(
                lambda x: f"{x['id']}: {x['score']}",
                data.values()
            )))

            if received_score_text != self.score_text.text:
                self.score_text.text = received_score_text

    # Bullet thread
    def network_bullet(self):
        # Todo
        pass
        # while True:
        #     # Update rate
        #     sleep(.001)
        #
        #     # Receive server information
        #     data = server.receive()
        #
        #     for enemy in data.values():
        #         enemy_id = enemy["id"]
        #         enemy["pos"][1] += 1
        #
        #         # Check if it's a bullet package
        #         # Ignore himself
        #         # Check if enemy exists
        #         if "bullet" in enemy.keys() and \
        #                 enemy_id != self.nickname and \
        #                 enemy_id in self.enemies:
        #             Bullet(
        #                 player=enemy,
        #                 position=tuple(enemy["bullet"]["pos"]),
        #                 rotation=tuple(enemy["bullet"]["rot"]),
        #                 ignore_collision=True
        #             )
