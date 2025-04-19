import pygame

from .game_object import GameObject
from .invader_bullets import InvaderBullet

INVADER_CLIPS = {
    "invader_1": [pygame.Rect(7, 225, 16, 16), pygame.Rect(40, 225, 16, 16)],
    "invader_2": [pygame.Rect(74, 225, 22, 16), pygame.Rect(107, 225, 22, 16)],
    "invader_3": [pygame.Rect(147, 226, 24, 16), pygame.Rect(179, 226, 24, 16)]
}

INVADER_POINTS = {
    "invader_1": 10,
    "invader_2": 20,
    "invader_3": 40
}


class Invader(GameObject):
    containers = None
    time = 0
    current_clip_index = 0
    direction_x = 1
    can_jump = False

    def __init__(self, position: tuple[float, float],
                 invader_id: str,
                 img_size=(28, 22),
                 speed=6):
        super().__init__(position, img_size, INVADER_CLIPS[invader_id], Invader.containers)
        self.speed = speed
        self.invader_points = INVADER_POINTS[invader_id]

    def update(self):
        if Invader.can_jump:
            self.jump_y()
        elif self.should_change_clip():
            self.move_x()
            self.animate()

    def animate(self):
        self.current_clip_index = 0 if self.current_clip_index == 1 else 1
        self.sprite_sheet.set_clip(self.clips[self.current_clip_index])
        image = self.sprite_sheet.subsurface(self.sprite_sheet.get_clip())
        self.image = pygame.transform.scale(image, self.img_size)

    def move_x(self):
        self.rect.move_ip(self.speed * Invader.direction_x, 0)

    def jump_y(self):
        self.rect.move_ip(0, 2 * self.speed)

    def should_change_clip(self) -> bool:
        if (pygame.time.get_ticks() - self.time) >= 800:
            self.time = pygame.time.get_ticks()
            return True
        return False

    def get_score(self) -> int:
        return self.invader_points

    def shoot(self):
        InvaderBullet(self.rect.midbottom)
