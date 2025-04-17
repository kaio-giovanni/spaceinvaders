import pygame

from src.sprites.bullet import Bullet
from src.sprites.game_object import GameObject


class SpaceShip(GameObject):
    containers = None

    def __init__(self, position: tuple[float, float], img_size=(52, 32), speed=6):
        super().__init__(position,
                         img_size,
                         [pygame.Rect(277, 228, 26, 16)],
                         SpaceShip.containers)
        self.speed = speed

    def update(self):
        pass

    def animate(self):
        pass

    def die(self):
        self.kill()

    def shoot(self):
        Bullet(position=self.rect.midtop, color=(0, 250, 154))

    def _move_up(self) -> None:
        self.rect.move_ip(0, -self.speed)

    def _move_down(self) -> None:
        self.rect.move_ip(0, self.speed)

    def move_left(self) -> None:
        self.rect.move_ip(-self.speed, 0)

    def move_right(self) -> None:
        self.rect.move_ip(self.speed, 0)
