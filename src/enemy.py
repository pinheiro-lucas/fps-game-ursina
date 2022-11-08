from ursina import *


class Enemy(Entity):
    def __init__(self, pos):
        super().__init__(world_position=pos, model="cube")
