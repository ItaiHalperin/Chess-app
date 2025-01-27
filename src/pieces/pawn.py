from src.piece import Piece
from src.boardposition import BoardPosition
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, game_board, origin, destination):
        if origin != destination and origin.in_board() and destination.in_board():
            dest_piece = game_board.board[destination.get_row()][destination.get_col()]
            turn = game_board.turn
            pawn_first_line = 1
            regular_row_increase = 1
            first_row_increase = 2

            if game_board.turn.color == 0:
                pawn_first_line = 6
                regular_row_increase = -1
                first_row_increase = -2

            return (origin.get_row() == destination.get_row() - regular_row_increase and origin.get_col() == destination.get_col() and
                    game_board.not_in_way(origin, destination, regular_row_increase, 0)) or \
                   (origin.get_row() == pawn_first_line and origin.get_row() == destination.get_row() - first_row_increase and
                    origin.get_col() == destination.get_col() and
                    game_board.not_in_way(origin, destination, regular_row_increase, 0)) or \
                   (origin.get_row() == destination.get_row() - regular_row_increase and
                    ((origin.get_col() == destination.get_col() - 1 and game_board.not_in_way(origin, destination, regular_row_increase, 1)) or
                     (origin.get_col() == destination.get_col() + 1 and game_board.not_in_way(origin, destination, regular_row_increase, -1))) and
                    dest_piece is not None and dest_piece.color != turn.color)
        return False

    def is_any_move_prevent_mate(self, game_board, pos):
        direction = 1
        if self.color == 0:
            direction = -1
        return self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + direction, pos.get_col())) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + 2 * direction, pos.get_col()))
