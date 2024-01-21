import pygame

class Letter(pygame.sprite.Sprite):
    def __init__(self, letter: str, pos: tuple[int, int], groups: pygame.sprite.AbstractGroup[...],
                 font: str, font_size: int, font_color: str) -> None:
        super().__init__(groups)
        font = pygame.font.Font(font, font_size)
        self.image = font.render(letter, True, font_color)
        self.rect = self.image.get_rect(topleft=pos)

        self.sprites = (font.render(letter, True, font_color, "red"),
                        self.image.copy(),
                        font.render(letter, True, font_color, "green"))

    def update_image(self, index: int) -> None:
        self.image = self.sprites[index]

    def update(self) -> None:
        pass

