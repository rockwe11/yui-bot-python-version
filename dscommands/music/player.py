import wavelink


class Player(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()
