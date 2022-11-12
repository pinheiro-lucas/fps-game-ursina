from ursina import *


class Map:
    def __init__(self):
        # self.sun = DirectionalLight().look_at(Vec3(0, 100, 0))
        self.sky = Sky(texture="sky_sunset", color=color.rgb(0, 255, 255))
        self.map = Entity(
            name="map",
            position=(0, 0, 0),
            model="models/map.obj",
            collider="models/map.obj",
            texture="grass",
            color=color.rgb(0, 0, 0),
            scale=7
        )
