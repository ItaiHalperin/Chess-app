from src.abs_board import AbsBoard
from src.pieces.directional_piece import DirectionalPiece
from src.player import BoardPosition


class Queen(DirectionalPiece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition) -> bool:
        return self.is_valid_diagonal_move(origin, destination, game_board) or self.is_valid_rectangular_move(origin, destination, game_board)

    def is_any_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition) -> bool:
        return self.is_any_rectangular_move_prevent_mate(game_board, pos) or self.is_any_diagonal_move_prevent_mate(game_board, pos)
