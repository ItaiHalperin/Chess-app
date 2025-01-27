from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.boardposition import BoardPosition
from src.abs_board import AbsBoard


class Piece(ABC):
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    @abstractmethod
    def is_any_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        pass

    @abstractmethod
    def is_valid_move(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition):
        pass

    def is_move_prevent_mate(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition):
        mat = game_board.board
        turn = game_board.turn
        origin_piece = mat[origin.get_row()][origin.get_col()]
        if origin_piece.is_valid_move(game_board, origin, destination):
            tmp_piece = mat[destination.get_row()][destination.get_col()]
            self.simulate_move(game_board, origin, destination)
            from src.pieces.king import King
            is_king_safe = King(turn.color).is_king_safe(game_board, turn)
            self.revert_move(game_board, origin, destination, tmp_piece)
            return is_king_safe
        return False

    @staticmethod
    def simulate_move(game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition):
        mat = game_board.board
        turn = game_board.turn

        mat[destination.get_row()][destination.get_col()] = mat[origin.get_row()][origin.get_col()]
        mat[origin.get_row()][origin.get_col()] = None
        if turn.king_pos.equals_to(origin):
            turn.king_pos = destination

    @staticmethod
    def revert_move(game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition, tmp_piece:Optional[Piece]):
        mat = game_board.board
        turn = game_board.turn
        mat[origin.get_row()][origin.get_col()] = mat[destination.get_row()][destination.get_col()]
        mat[destination.get_row()][destination.get_col()] = tmp_piece
        if turn.king_pos.equals_to(destination):
            turn.king_pos = origin


