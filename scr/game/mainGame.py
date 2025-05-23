from time import time
import pygame
from sys import exit

from scr.gameUI.pauseMenu import PauseMenu

from scr.game.oneLineBoard import OneLineBoard
from scr.gameUI.resultsMenu import ResultsMenu
from scr.support import show_text, Mouse
from scr.userconfig import user_config


class Game:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.update_sprites = pygame.sprite.Group()

        self.mouse = Mouse(self.update_sprites)

        self.pause_menu = PauseMenu(self.quit, self.start_game)
        self.result_menu = ResultsMenu(self.quit, self.start_game)

        self.start_game()

    def start_game(self) -> None:
        self.command = None
        self.running = True

        self.time_start = time()
        self.time_delay = 0
        self.paused = False

        self.finished = False

        self.texts = ("test1", "test2", "test3")
        self.board = OneLineBoard(self.texts)#FullScreenBoard(self.texts)

        pygame.mouse.set_visible(False)

    def quit(self, command) -> None:
        self.running = False
        self.command = command

    def timer(self) -> None:
        seconds = time() - self.time_start - self.time_delay
        minutes = seconds / 60
        seconds %= 60
        show_text(
            self.display,
            (10, 10),
            "arial",
            50,
            "black",
            None,
            f"Time: {int(minutes)}:{int(seconds) if int(seconds) > 9 else "0" + str(int(seconds))}"
        )

        self.time = seconds

    def key_input(self, event) -> None:
        keys = pygame.key.get_pressed()
        key = pygame.key.name(event.key)

        if keys[pygame.K_ESCAPE]:
            if self.paused:
                self.time_delay += time() - self.pause_time
                pygame.mouse.set_visible(False)
            else:
                self.pause_time = time()
                self.pause_menu.start()

            self.paused = not self.paused

        if not self.paused:
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                self.key_pressed = key.upper()

            elif keys[pygame.K_SPACE]:
                self.key_pressed = " "

            elif keys[pygame.K_BACKSPACE]:
                self.key_pressed = "<"

            else:
                self.key_pressed = key

    def check_finished(self) -> None:
        if self.board.finished and not self.finished:
            self.finished = True

            seconds = time() - self.time_start - self.time_delay

            words_per_minute = (60 * len(' '.join(self.texts).split())) / seconds
            self.result_menu.start(seconds, words_per_minute, self.board.mistakes)

    def show_fps(self) -> None:
        show_text(self.display,
                  (10, 60),
                  "arial",
                  25,
                  "black",
                  None,
                  f"FPS: {int(self.clock.get_fps())}"
                  )

    def run(self) -> str:
        while self.running:
            self.key_pressed = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    self.key_input(event)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.paused:
                        self.pause_menu.check_cursor()
                    elif self.finished:
                        self.result_menu.check_cursor()

            if not self.paused and not self.finished:
                self.display.fill("white")

                if self.key_pressed and len(self.key_pressed) == 1:
                    self.board.type(self.key_pressed)

                self.timer()
                self.show_fps()

                self.board.update()

            else:
                if self.paused:
                    self.pause_menu.run()
                else:
                    self.result_menu.run()

            self.check_finished()

            self.update_sprites.update(display=self.display)
            self.clock.tick(user_config.FPS)
            pygame.display.flip()

        return self.command
