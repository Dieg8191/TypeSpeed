import pygame
from json import loads
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


def get_texts(pack: str) -> list[str, ...]:
    with open(f"assets/texts/{pack}.json", 'r') as file:
        texts = loads(file.read())

    return texts["texts"]


def load_image(filename: str, new_scale: int | tuple[int, int] | None = None) -> pygame.surface.Surface:
    image = pygame.image.load(filename).convert_alpha()

    if not new_scale:
        return image
    elif isinstance(new_scale, int):
        size = image.get_size()
        new_scale = (new_scale * size[0], new_scale * size[1])

    return pygame.transform.scale(image, new_scale)


class Mouse(pygame.sprite.Sprite):
    def __init__(self, groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(groups)
        self.rect = pygame.rect.Rect(0, 0, 1, 1)

    def update(self, *args, **kwargs) -> None:
        self.rect.x, self.rect.y = pygame.mouse.get_pos()


class Tile(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: tuple[int, int],
                 groups: pygame.sprite.AbstractGroup) -> None:

        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)


