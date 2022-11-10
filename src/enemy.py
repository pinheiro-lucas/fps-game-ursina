from ursina import *


class Enemy(Entity):
    def __init__(self, pos, rot, name, rgb):
        self.e = super().__init__(
            name=name,
            world_position=pos,
            rotation=rot,
            color=color.rgb(*rgb),
            model="cube",
            scale=(1, 2, 1),
            collider="box"
        )

        self.gun = Entity(
            parent=self,
            position=Vec2(.6, -.5),
            scale=Vec3(.2, .2, .2),
            rotation=Vec3(10, 20, 5),
            model="models/ak47.obj",
            color=color.gray,
            on_cooldown=False
        )
