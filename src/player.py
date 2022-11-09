from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar

import json


class Player(FirstPersonController):
    def __init__(self, pos, nickname):
        # Todo: Nickname box in-game
        self._nickname = nickname
        self.online = True

        super().__init__(
            model="cube",
            speed=15,
            jump_height=2,
            jump_duration=.2,
            gravity=1,
            fall_after=.2,
            mouse_sensivity=Vec2(40, 40),
            height=2,
            position=pos
        )

        self._hp = 100

        self.collider = BoxCollider(self, (0, 1, 0), (1, 2, 1))

        # Destroy the old crosshair and build the new one
        destroy(self.cursor)
        self.cursor = Entity(
            parent=camera.ui,
            model="quad",
            texture="../materials/mira.png",
            scale=.025)

        self.health_bar = HealthBar(
            bar_color=color.red,
            roundness=.5,
            value=self._hp,
            show_text=False,
            position=(-.85, -.45)
        )

        self.gun = Entity(
            parent=camera.ui,
            position=Vec2(.6, -.5),
            scale=Vec3(.2, .2, .2),
            rotation=Vec3(10, 20, 5),
            model="models/ak47.obj",
            color=color.gray,
            on_cooldown=False
        )

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, n):
        self._hp = n

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, new_name):
        self._nickname = new_name

    def shoot(self):
        # Todo: Check if player is looking to grappling hook
        if not self.gun.on_cooldown:
            self.gun.on_cooldown = True
            self.gun.blink(color.orange)
            Bullet(
                model="sphere",
                scale=0.05,
                color=color.black,
                position=self.camera_pivot.world_position+Vec3(self.forward.x, 0, self.forward.z),
                rotation=self.camera_pivot.world_rotation
            )
            invoke(setattr, self.gun, "on_cooldown", False, delay=1)

    def to_json_str(self):
        player_info = {
            "id": self._nickname,
            "pos": tuple(self.position),
            "online": self.online
        }

        return json.dumps(player_info)

class Bullet(Entity):
    def __init__(self, speed=1500, lifetime=4,**kwargs):
        super().__init__(**kwargs)
        self.speed = speed
        self.lifetime = lifetime
        self.start = time.time()

    def update(self):
        ray = raycast(self.world_position, self.forward, distance=self.speed*time.dt, ignore=[self, 'player'])
        if not ray.hit and  time.time() - self.start < self.lifetime:
            self.world_position += self.forward * self.speed * time.dt
        else:
            destroy(self)
