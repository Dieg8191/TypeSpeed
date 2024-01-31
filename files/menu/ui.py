import pygame
from typing import Callable
from time import time
from config import FONTS
from support import load_image


class Button(pygame.sprite.Sprite):
    def __init__(self, button: str, pos: tuple[int, int], text: str, text_size: int,
                 command: Callable, groups: pygame.sprite.AbstractGroup):
        super().__init__(groups)
        root = "assets/sprites/buttons/"
        self.sprites = [load_image(path, 3) for path in (f"{root + button}1.png", f"{root + button}2.png")]

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.text = pygame.font.Font(FONTS["arial"], text_size).render(text, True, "black")
        self.text_rect = self.text.get_rect(center=self.rect.center)

        self.command = command
        self.start_timer_time = None
        self.timer = False

    def start_command_timer(self):
        self.start_timer_time = time()
        self.image = self.sprites[1]
        self.timer = True

    def update(self, *args, **kwargs):
        if self.timer:
            if time() - self.start_timer_time >= 0.15:
                self.command()

        kwargs["display"].blit(self.text, self.text_rect)
