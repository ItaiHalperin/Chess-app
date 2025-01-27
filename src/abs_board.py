from abc import ABC, abstractmethod

from src.player import BoardPosition


class AbsBoard(ABC):
    def __init__(self):
        self.turn = None
        self.board = None

    @abstractmethod
    def not_in_way(self, origin:BoardPosition, destination:BoardPosition, row_increase:int, col_increase:int):
        pass