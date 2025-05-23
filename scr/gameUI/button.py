from time import time
from typing import Callable

import pygame

from scr.support import load_image
from scr.userconfig import FONTS


class Button(pygame.sprite.Sprite):
    def __init__(self, button: str, pos: tuple[int, int], text: str, text_size: int,
                 command: Callable, groups: pygame.sprite.AbstractGroup):
        super().__init__(groups)
        root = "assets/sprites/buttons/"
        self.sprites = [load_image(path, 3) for path in (f"{root + button}1.png", f"{root + button}2.png")]

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=pos)

        x, y = self.sprites[0].get_size()
        x, y = x // 2, y // 2

        text_surface = pygame.font.Font(FONTS["arial"], text_size).render(text, True, "black")
        text_rect = text_surface.get_rect(center=(x, y))

        for image in self.sprites:
            image.blit(text_surface, text_rect)

        self.command = command
        self.start_timer_time = None
        self.timer = False

    def start_command_timer(self):
        self.start_timer_time = time()
        self.image = self.sprites[1]
        self.timer = True

    def update(self, *args, **kwargs):
        if self.timer:
            if time() - self.start_timer_time >= 0.2:
                self.command()