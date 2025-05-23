import pygame
from scr.game.letter import Letter


class OneLineBoard:
    def __init__(self, texts: tuple[str, ...] | str) -> None:
        # Board setup
        self.texts = texts if isinstance(texts, tuple) else (texts, )
        self.current_stage = 0
        self.stage_sprite_groups: list[list[Letter]] = []
        self.render_texts()
        self.visible_sprites: list[Letter] = self.stage_sprite_groups[self.current_stage]

        self.finished = False
        self.mistakes = 0

        # Display setup
        self.display = pygame.display.get_surface()

        #Cursor setup
        self.cursor_index = 0
        self.arrows_setup()

    def arrows_setup(self) -> None:
        self.up_arrow = pygame.image.load("assets/sprites/arrow.png").convert_alpha()
        self.down_arrow = pygame.transform.flip(self.up_arrow, False, True)

        bottom_upper_arrow = self.stage_sprite_groups[0][0].rect.top
        top_down_arrow = self.stage_sprite_groups[0][0].rect.bottom
        center_x = self.stage_sprite_groups[0][0].rect.centerx

        self.up_arrow_rect = self.up_arrow.get_rect(center=(center_x, bottom_upper_arrow - 40))
        self.down_arrow_rect = self.up_arrow.get_rect(center=(center_x, top_down_arrow + 40))

    def render_texts(self) -> None:
        y = pygame.display.get_surface().get_height() // 2

        for text in self.texts:
            x = pygame.display.get_surface().get_width() // 2
            sprites = []
            for char in text:
                letter = Letter(char, (0, 0), tuple(), "arial", 60, "black")
                letter.rect.centery = y
                letter.rect.left = x
                x += letter.rect.width
                sprites.append(letter)

            self.stage_sprite_groups.append(sprites)

    def draw_letters(self) -> None:
        for letter in self.visible_sprites:
            self.display.blit(letter.image, letter.rect)

    def update(self) -> None:
        self.draw_letters()

        self.display.blit(self.down_arrow, self.down_arrow_rect)
        #self.display.blit(self.up_arrow, self.up_arrow_rect)

    def move_letters(self, direction: int) -> None:
        if direction not in (-1, 1):
            raise ValueError("Direction must be -1 or 1")

        cursor_x: Letter = self.get_letter(self.cursor_index).rect.centerx
        other_x = self.get_letter(self.cursor_index + direction).rect.centerx

        offset = abs(other_x - cursor_x) * -direction
        print(offset)

        for letter in self.visible_sprites:
            letter.rect.x += offset

    def get_letter(self, i: int) -> Letter:
        return self.visible_sprites[i if i < len(self.visible_sprites) else len(self.visible_sprites) - 1]

    def type(self, key) -> None:
        letter: Letter = self.get_letter(self.cursor_index)

        if key == letter.letter and self.cursor_index < len(self.visible_sprites):
            letter.update_image(2)
        elif key != "<":
            letter.update_image(0)
            self.mistakes += 1

        if key == "<" and self.cursor_index > 0:
            self.move_letters(-1)
            self.cursor_index -= 1
            self.visible_sprites[self.cursor_index].update_image(1)

        elif self.cursor_index < len(self.visible_sprites) and key != "<":
            self.move_letters(1)
            self.cursor_index += 1

        if self.cursor_index >= len(self.visible_sprites):
            self.check_finished()

    def check_finished(self) -> None:
        if all(letter.index == 2 for letter in self.visible_sprites):
            self.current_stage += 1

            if self.current_stage < len(self.stage_sprite_groups):
                self.visible_sprites = self.stage_sprite_groups[self.current_stage]
                self.cursor_index = 0
                return

            self.finished = True
