import pygame

from .game_object import GameObject


class Explosion(GameObject):
    containers = None

    def __init__(self, sprite: GameObject):
        super().__init__(sprite.get_position(), sprite.get_img_size(), [pygame.Rect(480, 1140, 104, 64)],
                         Explosion.containers)
        self.anim_count = 6

    def update(self):
        if self.anim_count > 0:
            self.anim_count -= 1
        else:
            self.kill()
