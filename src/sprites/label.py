import pygame


class Label(pygame.sprite.Sprite):
    containers = None

    def __init__(self, text: str, font: pygame.font.Font, position, color) -> None:
        super().__init__(Label.containers)
        self.text = text
        self.font = font
        self.color = color
        self.image = font.render(text, True, color, None)
        self.rect = self.image.get_rect(center=position)

    def update(self) -> None:
        self.image = self.font.render(self.text, True, self.color, None)

    def set_text(self, text: str) -> None:
        self.text = text
