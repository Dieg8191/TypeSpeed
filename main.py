from files.game import Game
from files.menu import Menu
from config import SCREEN_SIZE, VERSION
import pygame


class App:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption(f"Type Speed v{VERSION}")
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

        self.game = Game(self.display, self.clock)
        self.menu = Menu(self.display, self.clock)

    def run(self) -> None:
        self.game.run()


if __name__ == '__main__':
    app = App()
    app.run()
