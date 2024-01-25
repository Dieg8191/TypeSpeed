import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple[int, int], groups: pygame.sprite.AbstractGroup):
        super().__init__(self, groups)

    def update(self):
        pass
