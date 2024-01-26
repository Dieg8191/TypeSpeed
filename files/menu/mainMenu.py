from random import choice
import pygame
from config import FPS, SCREEN_SIZE
from files.menu.ui import Button
from files.menu.backgroundKey import BackgroundKey
from support import Mouse, load_image


class Menu:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.on_menu = True

        self.mouse = Mouse()

        self.buttons = pygame.sprite.Group()
        self.background_keys = pygame.sprite.Group()

        for i in range(25):
            key = choice("aqxwgylt")
            BackgroundKey(key, self.background_keys)

        Button(load_image("assets/sprites/button1.png", (192, 64)), (10, 10), lambda: self.end_menu("play"), self.buttons)
        Button(load_image("assets/sprites/button1.png", (192, 64)), (200, 200), lambda: self.end_menu("quit"), self.buttons)

    def check_cursor(self) -> None:
        for button in self.buttons:
            if button.rect.colliderect(self.mouse.rect):
                button.command()

    def end_menu(self, command) -> None:
        self.on_menu = False
        self.command = command

    def run(self) -> str:
        while self.on_menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        self.check_cursor()

            delta_time = self.clock.tick(FPS) / 1000
            self.display.fill("white")

            self.mouse.update()

            self.background_keys.update(delta_time=delta_time)
            self.background_keys.draw(self.display)

            self.buttons.draw(self.display)

            pygame.display.flip()

        return self.command


