import sys
from Board import *
from Game import *
from Utilities import *
from TranspositionTable import *

TT = TranspositionTable()


class Phwar(QMainWindow):
    def __init__(self):
        super(Phwar, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.resize(600, 600)
        self.center()

        self.pboard = Board(11, 11, 2, self)
        #self.game = Game()

        # self.prules.make_connection_to_board(self.pboard)

        self.setCentralWidget(self.pboard)

        self.setWindowTitle('Phwar')
        self.show()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.resize(0.8*screen.height(), 0.8*screen.height())
        self.move(screen.width() - (1.15*size.width()), 0.05*size.height())


if __name__ == "__main__":
    app = QApplication([])
    phwar = Phwar()
    sys.exit(app.exec_())
