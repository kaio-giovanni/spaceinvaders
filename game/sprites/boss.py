import pygame
import random
from .game_object import GameObject


positions = [6000, 8000, 12000, 15000]


class Boss(GameObject):
    containers = None

    def __init__(self, pos_y, img_size=(48, 21), direction=-1, speed=6):
        # pos_x = random.choice(positions)
        super().__init__((900, pos_y), img_size, [pygame.Rect(215, 224, 48, 21)], Boss.containers)
        self.direction = direction
        self.speed = speed

    def update(self):
        self.move()
        if self.rect.x < 0:
            new_pos_x = random.choice(positions)
            self.rect.move_ip(new_pos_x, 0)

    def move(self):
        self.rect.move_ip(self.direction * self.speed, 0)

    def get_score(self) -> int:
        return 100

