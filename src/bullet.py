from ursina import *

from config import server


class Bullet(Entity):
    def __init__(self, player, ignore_collision=False, **kwargs):
        super().__init__(
            model="sphere",
            scale=.2,
            color=color.red,
            **kwargs
        )
        self.player = player
        self.speed = 500
        self.lifetime = 7
        self.start = time.time()
        self.ignore_collision = ignore_collision

    def update(self):
        ray = raycast(self.world_position, self.forward, distance=self.speed * time.dt, ignore=(self, self.player))

        time_left = time.time() - self.start

        if ray.hit or time_left > self.lifetime:
            # Object that have been hit
            hit = str(ray.entity)
            if not self.ignore_collision and hit not in ("None", "map", "player"):
                server.send({
                    "type": "hit",
                    "payload": {
                        "origin": self.player.nickname,
                        "target": hit
                    }
                })
            destroy(self)
        else:
            self.world_position += self.forward * self.speed * time.dt
