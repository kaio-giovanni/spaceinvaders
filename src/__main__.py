import os
import random
import time

import pygame

from src.sprites.boss import Boss
from src.sprites.bullet import Bullet
from src.sprites.explosion import Explosion
from src.sprites.game_object import GameObject
from src.sprites.invader import Invader
from src.sprites.invader_bullets import InvaderBullet
from src.sprites.label import Label
from src.sprites.life import Life
from src.sprites.spaceship import SpaceShip
from src.utils.utils import init, quit_game, create_font, create_player_lifes, remove_player_lifes, create_invaders

# SCREEN
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_SIZE = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

# COLORS
WHITE_COLOR = (255, 255, 255)
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
GOLD_COLOR = (255, 215, 0)
SPRINGREEN_COLOR = (0, 250, 154)

DIRECTORY = os.getcwd()

SPRITE_SHEET_PATH = DIRECTORY + "/assets/images/spritesheet.png"
SPRITE_SHEET = pygame.image.load(SPRITE_SHEET_PATH)
FONT_PATH = DIRECTORY + "/assets/fonts/space_invaders.ttf"


def menu_screen(surface: pygame.surface.Surface) -> None:
    black_screen = pygame.Surface(SCREEN_SIZE.size)
    black_screen.fill(BLACK_COLOR)

    game_logo_clip = pygame.Rect(173, 8, 229, 157)
    game_logo_image = SPRITE_SHEET.subsurface(game_logo_clip)
    invader_1 = SPRITE_SHEET.subsurface(pygame.Rect(7, 225, 16, 16))
    invader_2 = SPRITE_SHEET.subsurface(pygame.Rect(74, 225, 22, 16))
    invader_3 = SPRITE_SHEET.subsurface(pygame.Rect(147, 226, 24, 16))
    red_boss = SPRITE_SHEET.subsurface(pygame.Rect(215, 224, 48, 21))

    font = create_font(FONT_PATH, 20)
    text = font.render("Press Enter to start the game...", True, WHITE_COLOR, None)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

    font = create_font(FONT_PATH, 14)
    point_10 = font.render(" =        10 pts", True, WHITE_COLOR, None)
    point_20 = font.render(" =        20 pts", True, WHITE_COLOR, None)
    point_40 = font.render(" =        40 pts", True, WHITE_COLOR, None)
    point_boss = font.render(" =        ?? pts", True, WHITE_COLOR, None)

    x, y = game_logo_clip.centerx, game_logo_clip.bottom - 22

    point_10_rect = point_10.get_rect(center=(x + 140, y + 120))
    point_20_rect = point_20.get_rect(center=(x + 140, y + 168))
    point_40_rect = point_40.get_rect(center=(x + 140, y + 216))
    point_boss_rect = point_boss.get_rect(center=(x + 140, y + 264))

    black_screen.blit(game_logo_image, ((SCREEN_WIDTH / 2) - (game_logo_clip.width / 2), 30))
    black_screen.blit(pygame.transform.scale(invader_1, (24, 16)), (x + 24, y + 110))
    black_screen.blit(pygame.transform.scale(invader_2, (24, 16)), (x + 24, y + 158))
    black_screen.blit(pygame.transform.scale(invader_3, (24, 16)), (x + 24, y + 206))
    black_screen.blit(pygame.transform.scale(red_boss, (56, 22)), (x + 8, y + 254))

    black_screen.blit(point_10, point_10_rect)
    black_screen.blit(point_20, point_20_rect)
    black_screen.blit(point_40, point_40_rect)
    black_screen.blit(point_boss, point_boss_rect)
    black_screen.blit(text, text_rect)

    surface.blit(black_screen, (0, 0))
    pygame.display.flip()
    pygame.mouse.set_visible(True)
    pygame.key.set_repeat(10, 50)

    start_game = False
    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    start_game = True


def level_screen(surface: pygame.surface.Surface, level: int) -> None:
    black_screen = pygame.Surface(SCREEN_SIZE.size)
    black_screen.fill(BLACK_COLOR)

    font = create_font(FONT_PATH, 40)
    text = font.render("LEVEL {0}".format(level), True, WHITE_COLOR, None)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    black_screen.blit(text, text_rect)
    surface.blit(black_screen, (0, 0))
    pygame.display.flip()
    time.sleep(3)


def handle_keyboard_events(p: SpaceShip):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p.kill()
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                p.kill()
            elif keys[pygame.K_RIGHT] and p.rect.right < SCREEN_WIDTH:
                p.move_right()
            elif keys[pygame.K_LEFT] and p.rect.left > 0:
                p.move_left()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                p.shoot()


def game_screen(surface: pygame.surface.Surface, level: int) -> int:
    level_screen(surface, level)
    container_all = pygame.sprite.RenderUpdates()
    container_shields = pygame.sprite.Group()
    container_invaders = pygame.sprite.Group()
    container_bullets = pygame.sprite.Group()
    container_invader_bullets = pygame.sprite.Group()
    container_player = pygame.sprite.Group()
    container_life = pygame.sprite.Group()

    GameObject.sprite_sheet = SPRITE_SHEET

    SpaceShip.containers = container_all
    Bullet.containers = container_all, container_bullets
    InvaderBullet.containers = container_all, container_invader_bullets
    Invader.containers = container_all, container_invaders
    Boss.containers = container_all
    Label.containers = container_all
    Life.containers = container_all, container_life
    Explosion.containers = container_all

    player_initial_position = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
    player = SpaceShip(player_initial_position)

    black_screen = pygame.Surface(SCREEN_SIZE.size)
    black_screen.fill(BLACK_COLOR)
    surface.blit(black_screen, (0, 0))

    create_invaders()
    invader_direction = Invader.direction_x
    boss = Boss(20)

    score = 0
    score_label = Label("SCORE {0}".format(score), create_font(FONT_PATH, 12), (36, 16), GOLD_COLOR)
    Label("LEVEL {0}".format(level), create_font(FONT_PATH, 12), (SCREEN_WIDTH // 2, 16), WHITE_COLOR)

    fifo_lifes = create_player_lifes(3)

    num_invader_shooting = level * 5
    time_interval_invader_shooting = 3000  # 6k ms
    ticks = pygame.time.get_ticks()

    pygame.display.flip()
    clock = pygame.time.Clock()
    framerate = 60

    while player.alive() and len(container_invaders.sprites()) > 0:
        container_all.clear(surface, black_screen)
        container_all.update()
        Invader.can_jump = False
        handle_keyboard_events(player)

        for invader in container_invaders.sprites():
            if ((invader.rect.x > SCREEN_WIDTH - 50 and invader_direction > 0) or
                    (invader.rect.x < 20 and invader_direction < 0)):
                invader_direction *= -1
                Invader.direction_x = invader_direction
                Invader.can_jump = True
                break
            for bullet in pygame.sprite.spritecollide(invader, container_bullets, True):
                bullet.kill()
                invader.kill()
                Explosion(invader)
                score += invader.get_score()
                score_label.set_text("SCORE {0}".format(score))

        for invader_bullet in pygame.sprite.spritecollide(player, container_invader_bullets, True):
            invader_bullet.kill()
            life = remove_player_lifes(fifo_lifes)
            if life is not None:
                life.kill()
                Explosion(life)
            else:
                player.die()
                Explosion(player)

        for bullet in pygame.sprite.spritecollide(boss, container_bullets, True):
            bullet.kill()
            boss.kill()
            Explosion(boss)
            score += boss.get_score()
            score_label.set_text("SCORE {0}".format(score))

        if (pygame.time.get_ticks() - ticks) >= time_interval_invader_shooting:
            ticks = pygame.time.get_ticks()
            num_invaders = len(container_invaders.sprites())
            num_invader_shooting = num_invaders if num_invaders <= num_invader_shooting \
                else num_invader_shooting
            invaders_shooting = random.sample(container_invaders.sprites(), num_invader_shooting)
            for invader in invaders_shooting:
                invader.shoot()

        dirty = container_all.draw(surface)
        pygame.display.update(dirty)
        clock.tick(framerate)

    print("Game Over!")
    container_all.empty()
    container_shields.empty()
    container_invaders.empty()
    container_bullets.empty()
    container_player.empty()
    return score
    # quit_game()


def gameover_screen(surface: pygame.surface.Surface, total_score: int):
    black_screen = pygame.Surface(SCREEN_SIZE.size)
    black_screen.fill(BLACK_COLOR)

    font = create_font(FONT_PATH, 40)
    game_over_text = font.render("GAME OVER", True, WHITE_COLOR, None)
    font = create_font(FONT_PATH, 20)
    total_score_text = font.render("Total Score {0}".format(total_score), True, WHITE_COLOR, None)
    game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    total_score_text_rect = total_score_text.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 80))

    black_screen.blit(game_over_text, game_over_text_rect)
    black_screen.blit(total_score_text, total_score_text_rect)
    surface.blit(black_screen, (0, 0))
    pygame.display.flip()
    time.sleep(3)


def pygame_off():
    print("\t \t --- Pygame Module has been turned off ---")


if __name__ == '__main__':
    init()
    pygame.font.init()

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.register_quit(pygame_off)
    pygame.display.set_caption("Space Invaders")
    deep_display = pygame.display.mode_ok(SCREEN_SIZE.size, 0, 32)
    s = pygame.display.set_mode(SCREEN_SIZE.size, 0, deep_display)
    menu_screen(s)
    player_score = game_screen(s, 1)
    gameover_screen(s, player_score)
