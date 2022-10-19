from ursina import *
from ursina.shaders import lit_with_shadows_shader


class Map:
    def __init__(self):
        Entity.default_shader = lit_with_shadows_shader
        self.ground = Entity(model='plane',
                             scale=(100, 1, 100),
                             texture='grass',
                             texture_scale=(10, 10),
                             collider='box')
        self.sun = DirectionalLight().look_at(Vec3(1, -1, -1))
        self.sky = Sky(texture="sky_sunset")
