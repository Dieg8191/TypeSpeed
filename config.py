import pickle
from dataclasses import dataclass

VERSION = "0.3.0

font_root = "assets/fonts/"
FONTS = {
    "arial": f"{font_root}arial.ttf",
    "comic": f"{font_root}comic.ttf",
    "agency": f"{font_root}agency.ttf",
    "absolute": f"{font_root}Absolute 10 Basic.ttf",
    "pixel": f"{font_root}/pixel.fon"
}


@dataclass
class Config:
    FPS: int
    SCREEN_WIDTH: tuple[int, int]


def load_config() -> Config:
    try:
        with open("data/config.data", "rb") as file:
            file = pickle.load(file)

    except FileNotFoundError:
        file = Config(60, (1280, 720))
        save_config(file)

    return file


def save_config(data: Config) -> None:
    with open("data/config.data", "wb") as file:
        pickle.dump(data, file)

print(load_config().SCREEN_WIDTH)
