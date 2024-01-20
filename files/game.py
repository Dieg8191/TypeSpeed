from time import time
import pygame
from sys import exit
from support import show_text
from config import FPS


class Game:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.timer_start = time()

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

                    if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                        self.key_input = key.upper()

                    elif keys[pygame.K_SPACE]:
                        self.key_input = " "

                    else:
                        self.key_input = key

            self.display.fill("white")
            self.clock.tick(FPS)

            if self.key_input and len(self.key_input) == 1:
                print(self.key_input)

            self.timer()

            pygame.display.flip()
