import pygame

from scr.game.letter import Letter
from scr.support import Tile
from scr.userconfig import user_config, FONTS


class FullScreenBoard:
    def __init__(self, texts: tuple[str, ...] | str) -> None:
        x, y = user_config.SCREEN_SIZE[0] * .08, user_config.SCREEN_SIZE[1] * .08
        self.board = pygame.rect.Rect(x, y, user_config.SCREEN_SIZE[0] - (x * 2), user_config.SCREEN_SIZE[1] - (y * 1.5))
        self.board_surface = pygame.surface.Surface((self.board.width, self.board.height))

        self.mistakes = 0

        self.cursor_surface = pygame.Surface((10, 5))
        self.cursor_rect = self.cursor_surface.get_rect(topleft=(0, 0))

        self.display = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()

        self.texts = texts if isinstance(texts, tuple) else (texts, )
        self.stage = 0
        self.max_stage = len(self.texts)
        self.next_stage()

        self.finished = False

    def next_stage(self) -> None:
        if self.stage < self.max_stage:
            self.sprites.empty()
            text = self.texts[self.stage]

            self.letters = [Letter(text[0], (user_config.SCREEN_SIZE[0] * .10, 100), self.sprites, "arial", 60, "black")]

            y = 100
            for char in text[1::]:
                x = self.letters[-1].rect.right

                if x > user_config.SCREEN_SIZE[0] * .85 and self.letters[-1].letter == " ":
                    x = user_config.SCREEN_SIZE[0] * .10
                    y += self.letters[-1].rect.size[1]

                self.letters.append(Letter(char, (x, y), self.sprites,
                                           "arial", 60, "black"))

            self.finished = False
            self.index = 0
            self.stage += 1

            font = pygame.font.Font(FONTS["arial"], 50)
            text_surface = font.render(f"{self.stage}/{self.max_stage}", True, "black")
            Tile(text_surface, (user_config.SCREEN_SIZE[0] - 100, 25), self.sprites)

            self.update_cursor()
        else:
            self.finished = True

    def update_cursor(self) -> None:
        self.cursor_rect.topleft = self.letters[self.index].rect.bottomleft
        self.cursor_surface = pygame.transform.scale(self.cursor_surface,
                                                     (self.letters[self.index].rect.size[0], self.cursor_rect.size[1]))

    def type(self, key: str) -> None:
        if key == self.letters[self.index].letter:
            self.letters[self.index].update_image(2)
            self.index += 1

        elif key == "<":
            if self.letters[self.index].index == 1:
                self.index -= 1
            self.letters[self.index].update_image(1)

        elif self.letters[self.index].index == 1:
            self.letters[self.index].update_image(0)
            self.mistakes += 1
            self.index += 1

        if self.index < 0:
            self.index = 0

        elif self.index > len(self.letters) - 1:
            self.index = len(self.letters) - 1

        self.finished = all(map(lambda letter: letter.index == 2, self.letters))

        if self.finished:
            self.next_stage()
        else:
            self.update_cursor()

    def update(self) -> None:
        self.sprites.draw(self.display)
        self.display.blit(self.cursor_surface, self.cursor_rect)