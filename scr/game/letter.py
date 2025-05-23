import pygame
from scr.userconfig import FONTS


class Letter(pygame.sprite.Sprite):
    def __init__(self, letter: str, pos: tuple[int, int], groups: pygame.sprite.AbstractGroup,
                 font: str, font_size: int, font_color: str) -> None:
        super().__init__(groups)

        self.letter = letter
        font = pygame.font.Font(FONTS[font], font_size)
        self.index = 1
        self.sprites = (font.render(letter, True, font_color, "red"),
                        font.render(letter, True, font_color),
                        font.render(letter, True, font_color, "green"))
        self.image = self.sprites[1]
        self.rect = self.image.get_rect(topleft=pos)

    def update_image(self, index: int) -> None:
        self.image = self.sprites[index]
        self.index = index
