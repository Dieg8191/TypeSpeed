from files.game.mainGame import Game
from files.menu.mainMenu import Menu
from config import SCREEN_SIZE, VERSION
from ctypes import WinDLL
import pygame


class App:
    def __init__(self) -> None:
        # Adjust window dpi
        shcore = WinDLL('shcore')
        shcore.SetProcessDpiAwareness(1)

        # Initialize pygame modules
        pygame.init()
        pygame.font.init()

        # Creating thw window
        pygame.display.set_caption(f"Type Speed v{VERSION}")
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        running = True
        command = "menu"

        while running:
            match command:
                case "menu":
                    pygame.mouse.set_visible(True)
                    menu = Menu(self.display, self.clock)
                    command = menu.run()
                case "play":
                    game = Game(self.display, self.clock)
                    command = game.run()
                case "quit":
                    running = False
                case _:
                    raise ValueError(f"Unknown command: {command}")


if __name__ == '__main__':
    app = App()
    app.run()
