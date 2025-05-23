from typing import Callable, override
from scr.gameUI.button import Button
from scr.gameUI.inGameMenu import InGameMenu
from scr.support import show_text


class PauseMenu(InGameMenu):
    @override
    def __init__(self, quit_command: Callable, start_game: Callable) -> None:
        super().__init__()

        self.quit = quit_command
        self.start_game = start_game

    @override
    def start(self) -> None:
        super().start()
        Button("button", (200, 200), "quit", 19, lambda: self.quit("menu"), self.buttons)
        Button("button", (200, 400), "restart", 19, self.start_game, self.buttons)

    @override
    def run(self) -> None:
        super().run()

        show_text(self.display,
                  (100, 100),
                  "arial",
                  80,
                  "black",
                  None,
                  "Paused (Escape to unpause)"
                  )
