from ursina import *

class Map:
    def __init__(self):
        self.sun = DirectionalLight().look_at(Vec3(1, -1, -1))
        self.sky = Sky(texture="sky_sunset")
        self.map = Entity(
            position = (0, -70, 0),
            model = "models/map.obj",
            collider = "models/map.obj",
            texture = "grass",
            color = color.orange,
        )
