import pygame
from src.sprites.game_object import GameObject


class Life(GameObject):
    containers = None

    def __init__(self, position: tuple[float, float], img_size=(18, 14)):
        super().__init__(position, img_size, [pygame.Rect(281, 1148, 18, 14)], Life.containers)

    def update(self):
        pass
