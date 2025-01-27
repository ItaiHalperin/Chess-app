from src.abs_board import AbsBoard
from src.pieces.directional_piece import DirectionalPiece
from src.player import BoardPosition


class Bishop(DirectionalPiece):
    def __init__(self, color:int):
        super().__init__(color)

    def is_valid_move(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition):
        return self.is_valid_diagonal_move(origin, destination, game_board)

    def is_any_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        return self.is_any_diagonal_move_prevent_mate(game_board, pos)