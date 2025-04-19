import sys
import time
import collections
import pygame

from sprites.invader import Invader
from sprites.life import Life


def init():
    errors = pygame.init()
    if errors[1] > 0:
        print(f"(!) Ops, something is wrong... {errors}")
        return False
    else:
        print("(+) Pygame started successfully!")
        pygame.mixer.init()
        get_info_display()
        return True


def quit_game():
    time.sleep(1)
    pygame.quit()
    sys.exit(0)


def create_font(font_path: str, size: int):
    return pygame.font.Font(font_path, size)


def get_info_display():
    if pygame.display.get_init():
        print("Display Drivers", pygame.display.get_driver(), sep=" : ", end="\n")
        print("Display Info", pygame.display.Info(), sep=" : \n", end="\n")
        print("Display current window info", pygame.display.get_wm_info(), sep=" : ", end="\n")
    else:
        print("Pygame module crashed!!")


def create_invaders():
    invader_ids = ["invader_3", "invader_2", "invader_1", "invader_1"]
    for index, i in enumerate(invader_ids):
        for j in range(15):
            Invader(((j * 45) + 60, (index + 1) * 60), i)


def create_player_lifes(number_of_lifes: int) -> collections.deque:
    screen_width, h = pygame.display.get_surface().get_size()
    life_list = [Life((screen_width - (i * 24), 8)) for i in range(1, number_of_lifes + 1)]
    return collections.deque(life_list)


def remove_player_lifes(life_list: collections.deque) -> Life:
    try:
        return life_list.popleft()
    except IndexError:
        return None


def play_song(soundfile):
    if not (pygame.mixer.music.get_busy()):
        pygame.mixer.music.load(soundfile)
        pygame.mixer.music.play()
    else:
        pass
