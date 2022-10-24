from ursina import *


class Map:
    def __init__(self):
        self.ground = Entity(model='plane',
                             scale=(100, 1, 100),
                             texture='grass',
                             texture_scale=(10, 10),
                             collider='box')
        self.sun = DirectionalLight().look_at(Vec3(1, -1, -1))
        self.sky = Sky(texture="sky_sunset")
