import pygame
from userconfig import user_config, FONTS
from support import Tile, Mouse
from ui import Button
from support import show_text
from typing import Callable, override


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


class Board:
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


class InGameMenu:
    def __init__(self) -> None:
        self.display = pygame.display.get_surface()

        self.blur_surface = pygame.surface.Surface(self.display.get_size())
        self.blur_surface.fill("black")
        self.blur_surface.set_alpha(80)
        self.pause_rect = self.blur_surface.get_rect(topleft=(0, 0))

        self.buttons = pygame.sprite.Group()
        self.mouse = Mouse(())

    def start(self) -> None:
        pygame.mouse.set_visible(True)
        self.background = self.display.copy()

        self.buttons.empty()

    def check_cursor(self) -> None:
        for button in self.buttons:
            if button.rect.colliderect(self.mouse.rect):
                button.start_command_timer()

    def run(self) -> None:
        self.display.blit(self.background, (0, 0))
        self.display.blit(self.blur_surface, self.pause_rect)

        self.buttons.draw(self.display)
        self.mouse.update()
        self.buttons.update()


class ResultsMenu(InGameMenu):
    @override
    def __init__(self, quit_command: Callable, start_game: Callable) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()

        self.quit = quit_command
        self.start_game = start_game

    @override
    def start(self, time: int = 0, words_per_minute: int = 0, mistakes: int = 0) -> None:
        super().start()

        self.time = time
        self.words_per_minute = words_per_minute
        self.mistakes = mistakes

        Button("button", (400, 300), "quit", 19, lambda: self.quit("menu"), self.buttons)
        Button("button", (400, 400), "restart", 19, self.start_game, self.buttons)

    @override
    def run(self) -> None:
        super().run()

        show_text(self.display,
                  (250, 100),
                  "arial",
                  80,
                  "red",
                  None,
                  f"total time: {round(self.time, 3)} seconds"
                  )

        show_text(self.display,
                  (250, 200),
                  "arial",
                  80,
                  "red",
                  None,
                  f"Words/minute: {round(self.words_per_minute, 2)}"
                  )

        show_text(self.display,
                  (250, 0),
                  "arial",
                  80,
                  "red",
                  None,
                  f"Mistakes: {self.mistakes}"
                  )


class PauseMenu(InGameMenu):
    @override
    def __init__(self, quit_command: Callable, start_game: Callable) -> None:
        super().__init__()

        self.quit = quit_command
        self.start_game = start_game

    @override
    def start(self) -> None:
        super().start()
        Button("button", (200, 200), "quit", 19, lambda: self.quit("menu"), self.buttons)
        Button("button", (200, 400), "restart", 19, self.start_game, self.buttons)

    @override
    def run(self) -> None:
        super().run()

        show_text(self.display,
                  (100, 100),
                  "arial",
                  80,
                  "black",
                  None,
                  "Paused (Escape to unpause)"
                  )

