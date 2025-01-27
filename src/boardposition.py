from __future__ import annotations


class BoardPosition:
    def __init__(self, row, col):
        self._row = row
        self._col = col

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    def set_row(self, row:int):
        self._row = row

    def set_col(self, col:int):
        self._col = col

    def in_board(self):
        return 0 <= self._row < 8 and 0 <= self._col < 8

    def equals_to(self, pos:BoardPosition):
        return self._row == pos.get_row() and self._col == pos.get_col()

    def is_on_diagonal(self, pos):
        return abs(pos.get_row() - self._row) == abs(pos.get_col() - self._col)
