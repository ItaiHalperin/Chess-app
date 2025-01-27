from abc import ABC

from src.abs_board import AbsBoard
from src.piece import Piece
from src.boardposition import BoardPosition


class DirectionalPiece(Piece, ABC):
    def __init__(self, color:int):
        super().__init__(color)

    @staticmethod
    def is_valid_diagonal_move(origin:BoardPosition, destination:BoardPosition, game_board:AbsBoard):
        if not origin.equals_to(destination) and origin.in_board() and destination.in_board():
            row_increase = 0
            col_increase = 0
            if origin.is_on_diagonal(destination):
                if origin.get_row() < destination.get_row():
                    row_increase = 1
                else:
                    row_increase = -1

                if origin.get_col() < destination.get_col():
                    col_increase = 1
                else:
                    col_increase = -1
            return (row_increase != 0 or col_increase != 0) and game_board.not_in_way(origin, destination, row_increase, col_increase)
        return False

    @staticmethod
    def is_valid_rectangular_move(origin:BoardPosition, destination:BoardPosition, game_board:AbsBoard):
        if not origin.equals_to(destination) and origin.in_board() and destination.in_board():
            row_increase = 0
            col_increase = 0
            if origin.get_row() == destination.get_row():
                if origin.get_col() < destination.get_col():
                    col_increase = 1
                else:
                    col_increase = -1
            elif origin.get_col() == destination.get_col():
                if origin.get_row() < destination.get_row():
                    row_increase = 1
                else:
                    row_increase = -1
            return (row_increase != 0 or col_increase != 0) and game_board.not_in_way(origin, destination, row_increase, col_increase)
        return False

    def is_any_rectangular_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        return self.is_direction_prevent_mate(game_board, pos, 1, 0) or \
               self.is_direction_prevent_mate(game_board, pos, 0, 1)

    def is_any_diagonal_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        return self.is_direction_prevent_mate(game_board, pos, 1, 1) or \
               self.is_direction_prevent_mate(game_board, pos, 1, -1) or \
               self.is_direction_prevent_mate(game_board, pos, -1, 1) or \
               self.is_direction_prevent_mate(game_board, pos, -1, -1)

    def is_direction_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition, row_increase:int, col_increase:int):
        i = row_increase
        j = col_increase
        mat = game_board.board
        while 0 <= pos.get_row() + i < 8 and 0 <= pos.get_col() + j < 8:
            destination = BoardPosition(pos.get_row() + i, pos.get_col() + j)
            if self.is_move_prevent_mate(game_board, pos, destination):
                return True
            if mat[pos.get_row() + i][pos.get_col() + j] is not None:
                break
            i += row_increase
            j += col_increase
        return False
