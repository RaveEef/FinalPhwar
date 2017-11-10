from Move import *
from Board import *
from Utilities import *

class Game(QWidget):

    TILES = list()
    PIECES = list()

    def __init__(self, boardstack, parent=None):
        super(Game, self).__init__(parent)
        # QWidget.__init__(self, boardstack, parent)
        Game.TILES = list()
        set_player("B")
        self.boardstack = boardstack
        self.test_move = tuple()

        '''self.pieces = self.own_pieces()
        self.moves = list()

        self.all_moves()'''

    def start_ply(self):
        opponent = get_opponent()
        if opponent == "B":
            self.player = "W"

        moves = Move(self.boardstack)


