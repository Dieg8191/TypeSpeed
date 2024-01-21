from time import time
import pygame
from sys import exit
from support import show_text, Mouse
from config import FPS, FONTS
from files.game.text import Board


class Game:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.mouse = Mouse()

        self.timer_start = time()
        self.paused = False

        self.pause_surface = pygame.surface.Surface(self.display.get_size())
        self.pause_surface.fill("black")
        self.pause_surface.set_alpha(80)
        self.pause_rect = self.pause_surface.get_rect(topleft=(0, 0))

        self.board = Board("Hola mundo")

    def timer(self) -> None:
        seconds = time() - self.timer_start
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

    def run(self) -> None:
        while True:
            self.key_input = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    key = pygame.key.name(event.key)

                    if keys[pygame.K_ESCAPE]:
                        self.paused = not self.paused
                        self.display.blit(self.pause_surface, self.pause_rect)
                        show_text(self.display,
                                  (100, 100),
                                  "arial",
                                  80,
                                  "black",
                                  None,
                                  "Paused (Escape to unpause)"
                                  )

                    if not self.paused:
                        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                            self.key_input = key.upper()

                        elif keys[pygame.K_SPACE]:
                            self.key_input = " "

                        elif keys[pygame.K_BACKSPACE]:
                            self.key_input = "<"

                        else:
                            self.key_input = key

            self.clock.tick(FPS)

            if not self.paused:
                self.display.fill("white")
                if self.key_input and len(self.key_input) == 1:
                    #print(self.key_input)
                    self.board.input(self.key_input)

                self.timer()

                show_text(self.display,
                          (10, 60),
                          "arial",
                          25,
                          "black",
                          None,
                          f"FPS: {int(self.clock.get_fps())}"
                          )

                self.board.update()

            self.mouse.update()
            pygame.display.flip()
