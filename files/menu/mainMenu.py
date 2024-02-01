from random import choice
import pygame
from config import FPS
from ui import Button
from files.menu.backgroundKey import BackgroundKey
from support import Mouse, show_text


class Menu:
    def __init__(self, display: pygame.surface.Surface, clock: pygame.time.Clock) -> None:
        self.display = display
        self.clock = clock

        self.on_menu = True

        self.buttons = pygame.sprite.Group()
        self.update_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()

        self.mouse = Mouse(self.update_sprites)

        for i in range(45):
            key = choice(['a', 'q', 'x', 'w', 'g', 'y', 'l', 't'])
            BackgroundKey(key, (self.visible_sprites, self.update_sprites))

        Button("button", (100, 100), "play", 50, lambda: self.end_menu("play"),
               (self.visible_sprites, self.update_sprites, self.buttons))
        Button("button", (200, 200), "quit", 50, lambda: self.end_menu("quit"),
               (self.visible_sprites, self.update_sprites, self.buttons))

    def check_cursor(self) -> None:
        for button in self.buttons:
            if button.rect.colliderect(self.mouse.rect):
                button.start_command_timer()

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

            self.visible_sprites.draw(self.display)
            self.update_sprites.update(delta_time=delta_time, display=self.display)

            show_text(self.display,
                      (10, 10),
                      "arial",
                      25,
                      "black",
                      None,
                      f"FPS: {int(self.clock.get_fps())}"
                      )

            pygame.display.flip()

        return self.command


