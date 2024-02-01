from time import time
import pygame
from sys import exit
from support import show_text, Mouse
from config import FPS
from ui import Button
from files.game.GameUi import Board


class Game:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.command = None
        self.running = True

        self.update_sprites = pygame.sprite.Group()

        self.mouse = Mouse(self.update_sprites)
        pygame.mouse.set_visible(False)

        self.time_start = time()
        self.time_delay = 0
        self.paused = False

        self.pause_surface = pygame.surface.Surface(self.display.get_size())
        self.pause_surface.fill("black")
        self.pause_surface.set_alpha(80)
        self.pause_rect = self.pause_surface.get_rect(topleft=(0, 0))
        self.pause_buttons = pygame.sprite.Group()

        Button("button", (200, 200), "quit", 19, lambda: self.quit("menu"), self.pause_buttons)

        self.board = Board("a")

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

    def key_input(self, event) -> None:
        keys = pygame.key.get_pressed()
        key = pygame.key.name(event.key)

        if keys[pygame.K_ESCAPE]:
            if self.paused:
                self.time_delay += time() - self.pause_time
                pygame.mouse.set_visible(False)
            else:
                self.pause_time = time()
                self.display_copy = self.display.copy()
                pygame.mouse.set_visible(True)

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
            self.quit("menu")

    def check_cursor(self) -> None:
        for button in self.pause_buttons:
            if button.rect.colliderect(self.mouse.rect):
                button.start_command_timer()

    def show_fps(self) -> None:
        show_text(self.display,
                  (10, 60),
                  "arial",
                  25,
                  "black",
                  None,
                  f"FPS: {int(self.clock.get_fps())}"
                  )

    def pause_menu(self) -> None:
        self.display.blit(self.display_copy, (0, 0))
        self.display.blit(self.pause_surface, self.pause_rect)

        show_text(self.display,
                  (100, 100),
                  "arial",
                  80,
                  "black",
                  None,
                  "Paused (Escape to unpause)"
                  )
        self.pause_buttons.draw(self.display)
        self.pause_buttons.update()

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
                    self.check_cursor()

            if not self.paused:
                self.display.fill("white")

                if self.key_pressed and len(self.key_pressed) == 1:
                    self.board.type(self.key_pressed)

                self.timer()
                self.show_fps()

                self.board.update()

            else:
                self.pause_menu()

            self.check_finished()

            self.update_sprites.update(display=self.display)
            self.clock.tick(FPS)
            pygame.display.flip()

        return self.command
