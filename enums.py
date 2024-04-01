from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Difficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class Player(Enum):
    AI = 0
    PERSON = 1

class Heuristic(Enum):
    MISMATCHED_PIECES = 0
    MANHATTAN_DISTANCE = 1

class Algorithm(Enum):
    BFS = 0
    GREEDY = 1
    A_STAR = 2
