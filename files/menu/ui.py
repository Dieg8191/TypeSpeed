import pygame
from typing import Callable


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple[int, int],
                 command: Callable, groups: pygame.sprite.AbstractGroup):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

        self.command = command

    def update(self):
        pass
