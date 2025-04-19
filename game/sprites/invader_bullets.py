import pygame

from .game_object import GameObject


class InvaderBullet(GameObject):
    containers = None

    def __init__(self, position: tuple[float, float], img_size=(2, 12), direction=1, color=(255, 0, 0), speed=7):
        super().__init__(position, img_size, [pygame.Rect(183, 444, 4, 18)], InvaderBullet.containers)
        self.image.fill(color)
        self.rect = self.image.get_rect().move(position)
        self.direction = direction
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.direction * self.speed)
        if self.rect.y <= 0:
            self.kill()
