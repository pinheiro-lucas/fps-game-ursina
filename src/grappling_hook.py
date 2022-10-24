from ursina import *


class Ghook:
    def __init__(self, pos, p):
        self.entity = Button(
            parent=scene,
            model="cube",
            color=color.red,
            position=pos
        )

        self.entity.on_click = Func(
            p.animate_position,
            Vec3(
                self.entity.position.x,
                self.entity.position.y + 2,
                self.entity.position.z
            ),
            duration=.4,
            curve=curve.linear
        )
