import pygame
from config import FONTS


def show_text(display: pygame.surface.Surface, pos: tuple[int, int], font: str,
              font_size: int, color: str, background_color: str | None, text: str) -> None:

    font = pygame.font.Font(FONTS[font], font_size)

    if not background_color:
        text = font.render(text, True, color)
    else:
        text = font.render(text, True, color, background_color)

    text_rect = text.get_rect(topleft=pos)
    display.blit(text, text_rect)
