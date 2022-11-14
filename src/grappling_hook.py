from ursina import *


class Ghook:
    def __init__(self, hooks, p):
        for pos in hooks:
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
                    self.entity.position.y - 4,
                    self.entity.position.z
                ),
                duration=.4,
                curve=curve.linear
            )
