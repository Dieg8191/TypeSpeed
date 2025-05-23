import pygame
from typing import Callable, override

from scr.gameUI.button import Button
from scr.gameUI.inGameMenu import InGameMenu

from scr.support import show_text


class ResultsMenu(InGameMenu):
    @override
    def __init__(self, quit_command: Callable, start_game: Callable) -> None:
        super().__init__()
        self.display = pygame.display.get_surface()

        self.quit = quit_command
        self.start_game = start_game

    @override
    def start(self, time: int = 0, words_per_minute: int = 0, mistakes: int = 0) -> None:
        super().start()

        self.time = time
        self.words_per_minute = words_per_minute
        self.mistakes = mistakes

        Button("button", (400, 300), "quit", 19, lambda: self.quit("menu"), self.buttons)
        Button("button", (400, 400), "restart", 19, self.start_game, self.buttons)

    @override
    def run(self) -> None:
        super().run()

        show_text(self.display,
                  (250, 100),
                  "arial",
                  80,
                  "red",
                  None,
                  f"total time: {round(self.time, 3)} seconds"
                  )

        show_text(self.display,
                  (250, 200),
                  "arial",
                  80,
                  "red",
                  None,
                  f"Words/minute: {round(self.words_per_minute, 2)}"
                  )

        show_text(self.display,
                  (250, 0),
                  "arial",
                  80,
                  "red",
                  None,
                  f"Mistakes: {self.mistakes}"
                  )