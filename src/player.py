from src.boardposition import BoardPosition


class Player:
    def __init__(self, name:str, color:int):
        self.color = color
        self.is_checked = False
        self.games_won = 0
        self.player_name = name
        if self.color == 1:
            self.king_pos = BoardPosition(0, 4)
        else:
            self.king_pos = BoardPosition(7, 4)
