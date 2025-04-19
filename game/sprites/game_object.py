from abc import ABC, abstractmethod

import pygame


class GameObject(pygame.sprite.Sprite, ABC):
    sprite_sheet: pygame.surface.Surface = None

    def __init__(self, position: tuple[float, float],
                 img_size: tuple[float, float],
                 clips: list[pygame.Rect],
                 *containers) -> None:
        super().__init__(*containers)
        self.img_size = img_size
        self.clips = clips
        self.sprite_sheet = GameObject.sprite_sheet
        self.sprite_sheet.set_clip(clips[0])
        self.image = pygame.transform.scale(self.sprite_sheet.subsurface(self.sprite_sheet.get_clip()), img_size)
        self.rect = self.image.get_rect().move(position)

    @abstractmethod
    def update(self) -> None:
        pass

    def get_position(self) -> tuple[float, float]:
        return self.rect.x, self.rect.y

    def get_img_size(self) -> tuple[float, float]:
        return self.img_size
