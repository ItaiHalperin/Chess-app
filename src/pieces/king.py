from src.abs_board import AbsBoard
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.rook import Rook
from src.pieces.knight import Knight
from src.player import Player
from src.boardposition import BoardPosition
from src.piece import Piece
from src.pieces.pawn import Pawn


def is_pawn_bishop_distance(row_increase:int, col_increase:int):
    return abs(row_increase) == 1 and abs(col_increase) == 1


def is_valid_castling(game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition) -> bool:
    mat = game_board.board
    if abs(origin.get_col() - destination.get_col()) == 2 and origin.get_row() == destination.get_row() and isinstance(mat[origin.get_row()][origin.get_col()], King) and not mat[origin.get_row()][origin.get_col()].has_moved:
        col_increase = 1
        rook_col = 7
        if destination.get_col() < origin.get_col():
            col_increase = -1
            rook_col = 0

        if isinstance(mat[origin.get_row()][rook_col], Rook) and not mat[origin.get_row()][rook_col].has_moved:
            i = origin.get_row()
            j = origin.get_col() + col_increase
            while mat[i][j] is None and j != rook_col:
                j += col_increase
            return j == rook_col and not game_board.turn.is_checked
    return False


def is_rook_distance(row_increase:int, col_increase:int):
    return row_increase == 0 or col_increase == 0


class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def is_valid_move(self, game_board:AbsBoard, origin:BoardPosition, destination:BoardPosition) -> bool:
        if not origin.equals_to(destination) and origin.in_board() and destination.in_board():
            mat = game_board.board
            turn = game_board.turn
            if mat[destination.get_row()][destination.get_col()] is None or mat[destination.get_row()][destination.get_col()].color != turn.color:
                return (abs(origin.get_row() - destination.get_row()) <= 1 and abs(origin.get_col() - destination.get_col()) <= 1) or is_valid_castling(game_board, origin, destination)
        return False

    def is_king_safe(self, game_board:AbsBoard, player:Player) -> bool:
        king_pos = player.king_pos
        return self.safe_from_king(king_pos, game_board) and \
               self.safe_from_knight(king_pos, 2, 1, game_board) and \
               self.safe_from_knight(king_pos, 2, -1, game_board) and \
               self.safe_from_knight(king_pos, 1, 2, game_board) and \
               self.safe_from_knight(king_pos, 1, -2, game_board) and \
               self.safe_from_knight(king_pos, -2, 1, game_board) and \
               self.safe_from_knight(king_pos, -2, -1, game_board) and \
               self.safe_from_knight(king_pos, -1, 2, game_board) and \
               self.safe_from_knight(king_pos, -1, -2, game_board) and \
               self.safe_from_pawn(king_pos, 1, 1, game_board) and \
               self.safe_from_pawn(king_pos, 1, -1, game_board) and \
               self.safe_from_pawn(king_pos, -1, 1, game_board) and \
               self.safe_from_pawn(king_pos, -1, -1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos,1, 0,game_board) and \
               self.safe_from_rook_bishop_queen(king_pos,-1, 0,game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, 0, 1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, 0, -1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, 1, 1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, 1, -1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, -1, 1, game_board) and \
               self.safe_from_rook_bishop_queen(king_pos, -1, -1, game_board)

    def safe_from_immediate(self, king_pos:BoardPosition, row_increase:int, col_increase:int, game_board:AbsBoard) -> bool:
        mat = game_board.board
        destination = BoardPosition(king_pos.get_row() + row_increase, king_pos.get_col() + col_increase)
        if destination.in_board():
            if mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase] is not None:
                return mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase].color == self.color
        return True

    def safe_from_pawn(self, king_pos:BoardPosition, row_increase:int, col_increase:int, game_board:AbsBoard):
        mat = game_board.board
        endangering_position = BoardPosition(king_pos.get_row() + row_increase, king_pos.get_col() + col_increase)
        if endangering_position.in_board() and isinstance(mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase], Pawn):
            if (row_increase < 0 and mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase].color == 1) or \
                    (row_increase > 0 and mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase].color == 0):
                return self.safe_from_immediate(king_pos, row_increase, col_increase, game_board)
        return True

    def safe_from_king(self, king_pos:BoardPosition, game_board:AbsBoard):
        mat = game_board.board
        return (self.safe_from_immediate(king_pos, 1, -1, game_board) or not isinstance(mat[king_pos.get_row() + 1][king_pos.get_col() - 1], King)) and \
            (self.safe_from_immediate(king_pos, 1, 0, game_board) or not isinstance(mat[king_pos.get_row() + 1][king_pos.get_col()], King)) and \
            (self.safe_from_immediate(king_pos, 1, 1, game_board) or not isinstance(mat[king_pos.get_row() + 1][king_pos.get_col() + 1], King)) and \
            (self.safe_from_immediate(king_pos, 0, -1, game_board) or not isinstance(mat[king_pos.get_row()][king_pos.get_col() - 1], King)) and \
            (self.safe_from_immediate(king_pos, 0, 0, game_board) or not isinstance(mat[king_pos.get_row()][king_pos.get_col()], King)) and \
            (self.safe_from_immediate(king_pos, 0, 1, game_board) or not isinstance(mat[king_pos.get_row()][king_pos.get_col() + 1], King)) and \
            (self.safe_from_immediate(king_pos, -1, -1, game_board) or not isinstance(mat[king_pos.get_row() - 1][king_pos.get_col() - 1], King)) and \
            (self.safe_from_immediate(king_pos, -1, 0, game_board) or not isinstance(mat[king_pos.get_row() - 1][king_pos.get_col()], King)) and \
            (self.safe_from_immediate(king_pos, -1, 1, game_board) or not isinstance(mat[king_pos.get_row() - 1][king_pos.get_col() + 1], King))

    def safe_from_knight(self, king_pos:BoardPosition, row_increase:int, col_increase:int, game_board:AbsBoard):
        mat = game_board.board
        return self.safe_from_immediate(king_pos, row_increase, col_increase, game_board) or \
            not isinstance(mat[king_pos.get_row() + row_increase][king_pos.get_col() + col_increase], Knight)

    def safe_from_rook_bishop_queen(self, king_pos:BoardPosition, row_increase:int, col_increase:int, game_board:AbsBoard):
        i = row_increase
        j = col_increase
        mat = game_board.board
        while 0 <= king_pos.get_col() + j < 8 and 0 <= king_pos.get_row() + i < 8:
            if mat[king_pos.get_row() + i][king_pos.get_col() + j] is not None:
                if (isinstance(mat[king_pos.get_row() + i][king_pos.get_col() + j], Queen) or
                    (isinstance(mat[king_pos.get_row() + i][king_pos.get_col() + j], Rook) and is_rook_distance(row_increase, col_increase)) or
                    (isinstance(mat[king_pos.get_row() + i][king_pos.get_col() + j], Bishop) and is_pawn_bishop_distance(row_increase, col_increase))) and \
                        mat[king_pos.get_row() + i][king_pos.get_col() + j].color != self.color:
                    return False
                else:
                    break
            i += row_increase
            j += col_increase
        return True

    def is_any_move_prevent_mate(self, game_board:AbsBoard, pos:BoardPosition):
        row = pos.get_row()
        col = pos.get_col()
        return self.is_move_prevent_mate(game_board, pos, BoardPosition(row + 1, (col - 1))) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row + 1, col)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row + 1, col + 1)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row, col - 1)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row, col)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row, col + 1)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row - 1, col - 1)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row - 1, col)) or \
            self.is_move_prevent_mate(game_board, pos, BoardPosition(row - 1, col + 1))

