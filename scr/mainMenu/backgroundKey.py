import pygame
from scr.support import load_image
from scr.userconfig import user_config
from time import time
from random import randint


class BackgroundKey(pygame.sprite.Sprite):
    def __init__(self, key: str, groups: pygame.sprite.AbstractGroup) -> None:
        super().__init__(groups)
        root = "assets/sprites/background/"
        self.sprites = [load_image(path, (60, 60)) for path in (f"{root + key}1.png", f"{root + key}2.png")]
        angle = randint(-60, 60)

        for i in range(2):
            self.sprites[i] = pygame.transform.rotate(self.sprites[i], angle)
            self.sprites[i].set_alpha(150)

        self.image = self.sprites[0]
        self.rect = self.image.get_rect(topleft=(randint(0, user_config.SCREEN_SIZE[0]), randint(0, user_config.SCREEN_SIZE[1])))

        self.speed = randint(200, 300)

        self.press_delay = randint(1, 30)
        self.pressed = False

    def update(self, *args, **kwargs):
        if int(time()) % self.press_delay == 0 and not self.pressed:
            self.pressed = True
            self.image = self.sprites[1]
        elif int(time()) % self.press_delay != 0:
            self.pressed = False
            self.image = self.sprites[0]

        new_y_pos = self.speed * kwargs["delta_time"]
        self.rect.y += .51 if new_y_pos < .51 else new_y_pos

        if self.rect.top > user_config.SCREEN_SIZE[1]:
            self.rect.y = randint(0, user_config.SCREEN_SIZE[1] + 20)
            self.rect.x = randint(0, user_config.SCREEN_SIZE[0])
            self.rect.bottom = 0
            self.speed = randint(200, 300)
