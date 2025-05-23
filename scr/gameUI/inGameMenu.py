import pygame
from scr.support import Mouse


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