from dataclasses import dataclass
from enum import Enum
import chess

class Color(Enum):
    WHITE = "White"
    BLACK = "Black"

class Output(Enum):
    WIN = "Win"
    LOSE = "Lose"
    DRAW = "Draw"


@dataclass
class Game:
    color : Color
    output : Output
    moves : list[chess.Move]
