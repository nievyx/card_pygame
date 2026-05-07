from typing import Literal
from enum import Enum, auto

State = Literal['menu', 'game', 'how_to_play', 'quit']

class GameMode(Enum):
    WAVE_MODE = auto()
