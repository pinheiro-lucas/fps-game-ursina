from ursina import *


class Ghook:
    def __init__(self, pos, p):
        self.entity = Button(parent=scene,
                             model="cube",
                             color=color.red,
                             position=pos)
        self.entity.on_click = Func(p.animate_position, self.entity.position, duration=.4, curve=curve.linear)
