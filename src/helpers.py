from src.abs_board import AbsBoard
from src.pieces.pawn import Pawn
from src.boardposition import BoardPosition


def is_valid_final_rank_pawn(game_board:AbsBoard, origin: BoardPosition, destination: BoardPosition) -> bool:
    if isinstance(game_board.board[origin.get_row()][origin.get_col()], Pawn):
        pawn = game_board.board[origin.get_row()][origin.get_col()]
        is_valid_move = pawn.is_valid_move(game_board, origin, destination)
        if is_valid_move:
            return (destination.get_row() == 7 and game_board.board[origin.get_row()][origin.get_col()].color == 1) or (
                    destination.get_row() == 0 and game_board.board[origin.get_row()][origin.get_col()].color == 0)
    return False