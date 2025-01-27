from src.abs_board import AbsBoard
from src.pieces.directional_piece import DirectionalPiece
from src.player import BoardPosition


class Rook(DirectionalPiece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def is_valid_move(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition):
        return Rook.is_valid_rectangular_move(origin, destination, game_board)

    def is_any_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        return self.is_any_rectangular_move_prevent_mate(game_board, pos)

