import random

from dscommands.games.sapper.Cell import Cell


class Player:
    numbersS = [
        "0️⃣",
        "1️⃣",
        "2️⃣",
        "3️⃣",
        "4️⃣",
        "5️⃣",
        "6️⃣",
        "7️⃣",
        "8️⃣",
        "9️⃣"
    ]

    def __init__(self, player_id, bet):
        self.player_id = player_id
        self.bet = bet
        self.field = []
        self.create_field(5, 5)
        self.set_mines(5, 5, 5)
        self.count_mines_around(5, 5)

    def create_field(self, width, height):
        self.field = [[Cell() for _ in range(height)] for _ in range(width)]

    def set_mines(self, count, width, height):
        i = 0
        while i < count:
            Rx, Ry = random.choice(range(width)), random.choice(range(height))
            if not self.get_cell(Rx, Ry).is_mine:
                self.get_cell(Rx, Ry).is_mine = True
                self.get_cell(Rx, Ry).symb = "☢"
                i += 1

    def count_mines_around(self, width, height):
        for x in range(width):
            for y in range(height):
                if not self.get_cell(x, y).is_mine:
                    mines_around = 0
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if ((x + i) >= 0 and (y + j) >= 0) and ((x + i) < width and (y + j) < height):
                                if self.get_cell(x + i, y + j).is_mine:
                                    mines_around += 1
                    self.get_cell(x, y).mines_around = mines_around
                    self.get_cell(x, y).symb = self.numbersS[mines_around]

    def get_cell(self, x, y) -> Cell:
        return self.field[x][y]

    def get_player_id(self):
        return self.player_id
