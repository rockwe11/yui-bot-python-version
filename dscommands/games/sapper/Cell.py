class Cell:
    def __init__(self):
        self.fl = False
        self.is_mine = False
        self.is_open = False
        self.mines_around = 0
        self.symb = ""

    def get_mines_around(self):
        return self.mines_around

    def is_flag(self):
        return self.is_flag

    def get_symb(self):
        return self.symb
