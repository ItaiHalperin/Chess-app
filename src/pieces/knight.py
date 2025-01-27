from src.piece import Piece
from src.boardposition import BoardPosition
class Knight(Piece):
    def __init__(self, color):
        super().__init__(color)

    def is_valid_move(self, game_board, origin, destination):
        if origin.in_board() and destination.in_board():
            mat = game_board.board
            turn = game_board.turn
            if mat[destination.get_row()][destination.get_col()] is None or mat[destination.get_row()][destination.get_col()].color != turn.color:
                return (origin.get_row() + 2 == destination.get_row() and
                        (origin.get_col() + 1 == destination.get_col() or origin.get_col() - 1 == destination.get_col())) or \
                       (origin.get_row() + 1 == destination.get_row() and
                        (origin.get_col() + 2 == destination.get_col() or origin.get_col() - 2 == destination.get_col())) or \
                       (origin.get_row() - 2 == destination.get_row() and
                        (origin.get_col() + 1 == destination.get_col() or origin.get_col() - 1 == destination.get_col())) or \
                       (origin.get_row() - 1 == destination.get_row() and
                        (origin.get_col() + 2 == destination.get_col() or origin.get_col() - 2 == destination.get_col()))
        return False

    def is_any_move_prevent_mate(self, game_board, pos):
        return self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + 2, pos.get_col() + 1)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + 2, pos.get_col() - 1)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + 1, pos.get_col() + 2)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() + 1, pos.get_col() - 2)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() - 2, pos.get_col() + 1)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() - 2, pos.get_col() - 1)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() - 1, pos.get_col() + 2)) or \
               self.is_move_prevent_mate(game_board, pos, BoardPosition(pos.get_row() - 1, pos.get_col() - 2))
