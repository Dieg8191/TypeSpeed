import pygame
from config import FPS
from files.menu.gui import Button
from support import Mouse, load_image


class Menu:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.mouse = Mouse()

        self.buttons = pygame.sprite.Group()

        Button(load_image("assets/sprites/button.png"), (10, 10), lambda: print("!"), self.buttons)

    def check_cursor(self) -> None:
        for button in self.buttons:
            if button.rect.colliderect(self.mouse.rect):
                print("!")

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.display.fill("white")
            self.clock.tick(FPS)

            self.mouse.update()
            self.buttons.draw(self.display)
            self.check_cursor()

            pygame.display.flip()


