from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.prefabs.health_bar import HealthBar


class Player(FirstPersonController):
    def __init__(self, pos):
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

        self.collider = BoxCollider(self, (0, 1, 0), (1, 2, 1))

        # Destroy the old crosshair and build the new one
        destroy(self.cursor)
        self.cursor = Entity(
            parent=camera.ui,
            model="quad",
            texture="../materials/mira.png",
            scale=.025)

        self.health = HealthBar(
            bar_color=color.red,
            roundness=.5,
            value=100,
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

    def shoot(self):
        # Todo: Check if player is looking to grappling hook
        if not self.gun.on_cooldown:
            self.gun.on_cooldown = True
            self.gun.blink(color.orange)
            bullet = Entity(
                parent=camera,
                position=Vec3(.72, -.28, 2.2),
                model="cube",
                scale=.1,
                color=color.black,
                collider="box"
            )
            bullet.world_parent = scene
            bullet.animate_position(
                bullet.position + bullet.forward * 1000,
                curve=curve.linear,
                duration=1.5
            )
            destroy(bullet, delay=2)
            invoke(setattr, self.gun, "on_cooldown", False, delay=.20)
