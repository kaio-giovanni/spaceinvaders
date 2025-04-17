import pygame

from src.sprites.game_object import GameObject


class Bullet(GameObject):
    containers = None

    def __init__(self, position: tuple[float, float], img_size=(2, 12), direction=-1, color=(0, 250, 154), speed=8):
        super().__init__(position, img_size, [pygame.Rect(183, 444, 4, 18)], Bullet.containers)
        self.image.fill(color)
        self.rect = self.image.get_rect().move(position)
        self.direction = direction
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.direction * self.speed)
        if self.rect.y <= 0:
            self.kill()
