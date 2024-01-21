import pygame
from config import SCREEN_SIZE, FONTS


class Letter(pygame.sprite.Sprite):
    def __init__(self, letter: str, pos: tuple[int, int], groups: pygame.sprite.AbstractGroup,
                 font: str, font_size: int, font_color: str) -> None:
        super().__init__(groups)

        self.letter = letter
        font = pygame.font.Font(FONTS["arial"], font_size)
        self.index = 1
        self.sprites = (font.render(letter, True, font_color, "red"),
                        font.render(letter, True, font_color, "white"),
                        font.render(letter, True, font_color, "green"))
        self.image = self.sprites[1]
        self.rect = self.image.get_rect(topleft=pos)

    def update_image(self, index: int) -> None:
        self.image = self.sprites[index]
        self.index = index

    def update(self) -> None:
        pass


class Board:
    def __init__(self, text) -> None:
        x, y = SCREEN_SIZE[0] * .08, SCREEN_SIZE[1] * .08
        self.board = pygame.rect.Rect(x, y, SCREEN_SIZE[0] - (x * 2), SCREEN_SIZE[1] - (y * 1.5))
        self.board_surface = pygame.surface.Surface((self.board.width, self.board.height))

        self.display = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()

        self.start(text)

    def start(self, text: str) -> None:
        self.letters = [Letter(text[0], (100, 100), self.sprites, "arial", 40, "black")]
        for char in text[1::]:
            self.letters.append(Letter(char, (self.letters[-1].rect.right, 100), self.sprites,
                                       "arial", 40, "black"))

        self.index = 0

    def input(self, key: str) -> None:
        if key == self.letters[self.index].letter:
            self.letters[self.index].update_image(2)
            self.index += 1

        elif key == "<":
            if self.letters[self.index].index == 1:
                self.index -= 1
            self.letters[self.index].update_image(1)

        elif self.letters[self.index].index == 1:
            self.letters[self.index].update_image(0)
            self.index += 1

        if self.index < 0:
            self.index = 0

        elif self.index > len(self.letters) - 1:
            self.index = len(self.letters) - 1

        print(self.index)

    def update(self):
        self.sprites.draw(self.display)
