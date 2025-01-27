from typing import Optional, List

from src.abs_board import AbsBoard
from src.piece import Piece
from src.pieces.bishop import Bishop
from src.pieces.queen import Queen
from src.pieces.rook import Rook
from src.pieces.king import King
from src.pieces.knight import Knight
from src.pieces.pawn import Pawn
from src.player import Player
from src.boardposition import BoardPosition

class Board(AbsBoard):
    def __init__(self, p1: Player, p2: Player, board_dict=None):
        super().__init__()
        self.board: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        if p1.color == 0:
            self.black = p1
            self.white = p2
        else:
            self.white = p1
            self.black = p2
        self.turn = p1
        if board_dict:
            self.init_board(p1, board_dict)
        else:
            self.init_board()

    def init_board(self, turn:Player=None, board_dict:dict = None):
        if not board_dict:
            self.white.king_pos = BoardPosition(0, 4)
            self.black.king_pos = BoardPosition(7, 4)
            self.board[0][0] = Rook(1)
            self.board[0][1] = Knight(1)
            self.board[0][2] = Bishop(1)
            self.board[0][3] = Queen(1)
            self.board[0][4] = King(1)
            self.board[0][5] = Bishop(1)
            self.board[0][6] = Knight(1)
            self.board[0][7] = Rook(1)
            self.board[1] = [Pawn(1) for _ in range(8)]
            self.board[6] = [Pawn(0) for _ in range(8)]
            self.board[7][0] = Rook(0)
            self.board[7][1] = Knight(0)
            self.board[7][2] = Bishop(0)
            self.board[7][3] = Queen(0)
            self.board[7][4] = King(0)
            self.board[7][5] = Bishop(0)
            self.board[7][6] = Knight(0)
            self.board[7][7] = Rook(0)
        
        else:
            if board_dict.get('turn') == 0:
                self.turn = turn
            for row in range(8):
                for col in range(8):
                    if board_dict.get(str(row) + ", " + str(col)):
                        cur_piece = board_dict.get(str(row) + ", " + str(col)).get('piece')
                        if cur_piece[1:] == "king":
                            if cur_piece[0] == 'W':
                                self.white.king_pos = BoardPosition(row, col)
                            else:
                                self.black.king_pos = BoardPosition(row, col)

                        self.board[row][col] = Board.switch(cur_piece)
                        self.board[row][col].has_moved = board_dict.get(str(row) + ", " + str(col)).get('has_moved')
            self.white.is_checked = board_dict.get("isWhiteChecked")
            self.black.is_checked = board_dict.get("isBlackChecked")


    @staticmethod
    def switch(case):
        if case[0] == "W":
            color = 1
        else:
            color = 0
        return {
            'pawn': Pawn(color),
            'rook': Rook(color),
            'knight': Knight(color),
            'bishop': Bishop(color),
            'queen': Queen(color),
            'king': King(color)

        }.get(case[1:], 'Default case')

    def get_turn(self):
        return self.turn

    def not_in_way(self, origin:BoardPosition, destination, row_increase, col_increase):
        i, j = origin.get_row() + row_increase, origin.get_col() + col_increase
        destination_row = destination.get_row()
        destination_col = destination.get_col()
        while (self.board[i][j] is None) and (i != destination_row or j != destination_col):
            i += row_increase
            j += col_increase
        if (self.board[i][j] is not None) and (self.board[i][j].color == self.turn.color or (
                isinstance(self.board[origin.get_row()][origin.get_col()], Pawn) and col_increase == 0)):
            return False
        return i == destination_row and j == destination_col

    def is_checkmate(self):
        if not self.turn.is_checked:
            return False
        for i in range(8):
            for j in range(8):
                pos = BoardPosition(i, j)
                if (self.board[i][j] is not None and self.board[i][j].color == self.turn.color and
                        self.board[i][j].is_any_move_prevent_mate(self, pos)):
                    return False
        return True

    def move(self, origin, destination):
        p1 = self.white
        p2 = self.black
        if self.turn.color == 0:
            p1, p2 = p2, p1

        if self.board[origin.get_row()][origin.get_col()] is None or self.board[origin.get_row()][origin.get_col()].color != self.turn.color \
                or not self.board[origin.get_row()][origin.get_col()].is_valid_move(self, origin, destination):
            print("\nInvalid! Please try again.")
            return False

        if p1.is_checked and King(self.board[p1.king_pos.get_row()][p1.king_pos.get_col()].color).is_king_safe(self, p1):
            p1.is_checked = False

        if p2.is_checked and King(self.board[p1.king_pos.get_row()][p1.king_pos.get_col()].color).is_king_safe(self, p2):
            p2.is_checked = False

        tmp = self.board[destination.get_row()][destination.get_col()]
        self.board[destination.get_row()][destination.get_col()] = self.board[origin.get_row()][origin.get_col()]
        self.board[origin.get_row()][origin.get_col()] = None
        if isinstance(self.board[destination.get_row()][destination.get_col()], King):
            p1.king_pos = destination
        if King(self.board[p1.king_pos.get_row()][p1.king_pos.get_col()].color).is_king_safe(self, p1):
            self.board[destination.get_row()][destination.get_col()].has_moved = True
            if not King(self.board[p2.king_pos.get_row()][p2.king_pos.get_col()].color).is_king_safe(self, p2):
                p2.is_checked = True
            if self.is_castle_move(origin, destination):
                self.move_rook_castling(origin, destination)

            return True
        else:
            self.board[origin.get_row()][origin.get_col()] = self.board[destination.get_row()][destination.get_col()]
            self.board[destination.get_row()][destination.get_col()] = tmp
            if isinstance(self.board[origin.get_row()][origin.get_col()], King):
                p1.king_pos = origin
            print("\nInvalid! Please try again.")
            return False

    def render_board(self):
        keys = ["turn", "isWhiteChecked", "isBlackChecked"]
        values = [self.turn.color, self.white.is_checked, self.black.is_checked]
        for i in range(8):
            for j in range(8):
                if  self.board[i][j]:
                    piece = ""
                    if  isinstance(self.board[i][j], Pawn):
                        piece = "pawn"
                    if  isinstance(self.board[i][j], Rook):
                        piece = "rook"
                    if  isinstance(self.board[i][j], Knight):
                        piece = "knight"
                    if  isinstance(self.board[i][j], Bishop):
                        piece = "bishop"
                    if  isinstance(self.board[i][j], King):
                        piece = "king"
                    if  isinstance(self.board[i][j], Queen):
                        piece = "queen"
                
                    keys.append(str(i) + ", "+ str(j))
                    if self.board[i][j].color == 0:
                        color = 'B'
                    else:
                        color = 'W'
                    values.append({"piece": color + piece, 'has_moved': self.board[i][j].has_moved})
        pieces = dict(zip(keys, values))
        return pieces
    def move_rook_castling(self, origin, destination):
        col_increase = 1
        rook_col = 7
        if destination.get_col() < origin.get_col():
            col_increase = -1
            rook_col = 0

        self.board[origin.get_row()][destination.get_col() - col_increase] = self.board[origin.get_row()][rook_col]
        self.board[origin.get_row()][rook_col] = None
        self.board[origin.get_row()][destination.get_col() - col_increase].has_moved = True

    def is_castle_move(self, origin, destination):
        return isinstance(self.board[destination.get_row()][destination.get_col()], King) and abs(destination.get_col() - origin.get_col()) == 2

    def change_turn(self):
        if self.turn.color == 0:
            self.turn = self.white
        else:
            self.turn = self.black

    def replace_pawn(self, piece:str, origin, destination):
        p1 = self.white
        p2 = self.black
        if self.turn.color == 0:
            p1, p2 = p2, p1
        pawn = self.board[origin.get_row()][origin.get_col()]
        self.board[origin.get_row()][origin.get_col()] = None
        replacing_piece = ""
        if piece == "queen":
            replacing_piece = Queen(pawn.color)
        elif piece == "knight":
            replacing_piece = Knight(pawn.color)
        elif piece == "bishop":
            replacing_piece = Bishop(pawn.color)
        elif piece == "rook":
            replacing_piece = Rook(pawn.color)
        self.board[destination.get_row()][destination.get_col()] = replacing_piece
        king_row = p2.king_pos.get_row()
        king_col = p2.king_pos.get_col()
        if not King(self.board[king_row][king_col].color).is_king_safe(self, p2):
            p2.is_checked = True
