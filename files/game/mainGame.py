from time import time
import pygame
from sys import exit
from support import show_text, Mouse
from config import FPS
from ui import Button
from files.game.gameUi import Board, PauseMenu


class Game:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.update_sprites = pygame.sprite.Group()

        self.mouse = Mouse(self.update_sprites)

        self.pause_menu = PauseMenu(self.quit, self.start_game)

        self.start_game()

    def start_game(self) -> None:
        self.command = None
        self.running = True

        self.time_start = time()
        self.time_delay = 0
        self.paused = False

        self.texts = ("hola pepe", "hola")
        self.board = Board(self.texts)

        pygame.mouse.set_visible(False)

    def quit(self, command) -> None:
        self.running = False
        self.command = command

    def timer(self) -> None:
        seconds = time() - self.time_start - self.time_delay
        minutes = seconds / 60
        seconds %= 60
        show_text(self.display,
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
        if self.board.finished:
            print(f"time: {self.time}")
            print(f"w/m: {(60 * len(' '.join(self.texts).split())) / self.time}")
            self.quit("menu")

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
                    self.pause_menu.check_cursor()

            if not self.paused:
                self.display.fill("white")

                if self.key_pressed and len(self.key_pressed) == 1:
                    self.board.type(self.key_pressed)

                self.timer()
                self.show_fps()

                self.board.update()

            else:
                self.pause_menu.run()

            self.check_finished()

            self.update_sprites.update(display=self.display)
            self.clock.tick(FPS)
            pygame.display.flip()

        return self.command
