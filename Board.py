# from Move import Move
# from BoardTree import *
from PyQt4.QtCore import Qt, QPoint, QPointF, QRect, QRectF
from PyQt4.QtGui import QFrame, QPainter, QPainterPath, QPen, QBrush, QFont
from Utilities import *
from BoardTree import *
from TranspositionTable import *
from Game import *
from math import sqrt, cos, sin, pi


class Board(QFrame):

    set_player('B')
    PIECES = ['BN', 'BP1', 'BP2', 'BE1', 'BE2', 'BE3', 'BP3', 'BP4', 'BE4',
              'WN', 'WP1', 'WP2', 'WE1', 'WE2', 'WE3', 'WP3', 'WP4', 'WE4']

    # OWN_PIECES = [('BP3', 'E6')]
    OWN_PIECES = [('BE1', 'D2'), ('BP1', 'E1'), ('BE2', 'F2'), ('BN', 'G1'), ('BE4', 'F3'), ('BP4', 'G2'),
                  ('BP2', 'H2'), ('BE3', 'I2'), ('BP3', 'D4'), ('WE1', 'D10'), ('WP3', 'E9'), ('WP1', 'E10'),
                  ('WE4', 'G9'), ('WE2', 'F10'), ('WN', 'F11'), ('WP2', 'G10'), ('WE3', 'I9'), ('WP4', 'H4')]

    def __init__(self, nr, nc, s, parent):

        super(Board, self).__init__(parent)
        self.resize(parent.size())
        self.setFocusPolicy(Qt.StrongFocus)

        global NR, NC
        NR = nr
        NC = nc
        set_board_size(NR, NC)

        self.NR_COORD = (2 * NR) - 1
        self.S = s
        self.selected = None
        self.tiles = list()
        self.stack = BoardStack()

        self.init_tiles()
        self.init_pieces()

        global TT, TREE
        print TT.get_zhash(list(self.tiles))
        TREE.root(self.tiles)

        #own_initial_pieces(self.tiles, Board.OWN_PIECES)

        # Writing the initial board to boards.txt
        # file = open("boards.txt", "w")
        # file.write("\n{:^65}\n".format("INITIAL BOARD"))
        # file.write(print_hex(Board.TILES))
        # file.close()

        # print "\n{:^65}\n".format("INITIAL BOARD")
        # print print_hex(Board.TILES)

        self.setMouseTracking(True)

    @property
    def r_hex(self):
        tile_h = (self.contentsRect().height() - ((NR + 1) * self.S)) / NR
        tile_w = (2 * tile_h) / sqrt(3)
        return tile_w / 2

    # region Initializing the tiles and pieces
    def init_tiles(self):

        for j in range(NC):
            first_row = abs(j - (NC / 2))
            last_row = (2 * NC) - first_row - 1
            for i in range(first_row, last_row, 2):
                name = str(chr(65+j)) + str((i/2) + 1)                                              #chr(65) = A
                d = (NC/2) - j

                # region Description of coordinate computation
                # For all columns on the left side, d is positive, so x-value decreases and vice versa
                # Initialize the vertical position to the minimum distance to the upper bound of the frame
                # (spacing +half hexagon height)
                # With every second column, relative to the mid, the first tile is completely positioned below the
                # first tile 2 columns before
                # The row's vertical position below the one above it (and includes spacing)
                # If we are at an odd distance from the column in the middle, the initial offset is increased by half
                # the spacing plus half hexagon height
                # endregion
                real_x = (self.contentsRect().width() / 2) - (d * (self.S + self.r_hex)) - ((d * self.r_hex) / 2)
                real_y = self.S + ((sqrt(3) * self.r_hex) / 2)
                real_y += (abs(d)/ 2)*(self.S + (sqrt(3) * self.r_hex))
                real_y += (((i - first_row) / 2) * (self.S + (sqrt(3) * self.r_hex)))
                if d % 2 != 0:
                    real_y += (self.S + (sqrt(3) * self.r_hex)) / 2

                self.add_tile(name, QPoint(i, j), self.tile_path(real_x, real_y), QPointF(real_x, real_y))

    def init_pieces(self):
        mid_col = NC / 2
        initial_pos = [(0, mid_col),
                       (1, mid_col-1), (1,mid_col+1),
                       (2, mid_col-2), (2, mid_col), (2, mid_col+2),
                       (3, mid_col-1), (3, mid_col+1),
                       (4, mid_col)]
        for index, c in enumerate(initial_pos):
            black_tile = [t for t in self.tiles if t.coord.x() == c[0] and t.coord.y() == c[1]][0]
            #if black_tile.name == "E2":
            #    black_tile = [t for t in self.tiles if t.coord.x() == 11 and t.coord.y() == 4][0]

            self.add_piece(Board.PIECES[index], black_tile)

            white_tile = [t for t in self.tiles if
                          t.coord.x() == (self.NR_COORD - 1 - c[0]) and t.coord.y() == c[1]][0]
            white_index = index + (Board.PIECES.__len__() / 2)
            self.add_piece(Board.PIECES[white_index], white_tile)
    # endregion

    # region Adding tiles to the board and pieces to the tiles
    def add_tile(self, name, coord, path, pos):
        t = TileItem()
        t.set_name(name)
        t.set_coord(coord)
        t.set_pos(pos)
        t.set_path(path)
        t.set_color(Qt.white)
        t.set_piece(None)

        self.tiles.append(t)

    def add_piece(self, piece, tile):
        p = PieceItem(name=piece)
        p.set_tile(tile)
        tile.set_piece(p)
    # endregion

    # region Paint Functions
    def tile_path(self, cx, cy):
        path = QPainterPath()
        path.moveTo((cx - self.r_hex), cy)
        for i in range(1,6):
            x = cx + (self.r_hex * cos(((3 - i) * pi) / 3))
            y = cy + (self.r_hex * sin(((3 - i) * pi) / 3))
            path.lineTo(x, y)
        path.closeSubpath()
        return path

    def piece_circle_path(self, tile):
        path = QPainterPath()
        path.moveTo(tile.pos)
        path.addEllipse(tile.pos, 0.75 * self.r_hex, 0.75 * self.r_hex)
        path.closeSubpath()
        return path

    def piece_sign_path(self, tile):
        if tile.piece.sign == "N":
            return QPainterPath()
        else:
            path = QPainterPath()
            path.moveTo(tile.pos.x() - self.r_hex / 2, tile.pos.y())
            path.lineTo(tile.pos.x() + self.r_hex / 2, tile.pos.y())

            if tile.piece.sign == "E":
                return path
            else:
                vertical_line = QPainterPath()
                vertical_line.moveTo(tile.pos.x(), tile.pos.y() - self.r_hex / 2)
                vertical_line.lineTo(tile.pos.x(), tile.pos.y() + self.r_hex / 2)
                path += vertical_line
                return path

    def paint_tiles(self, painter):
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(Qt.white))

        # for tile in Board.TILES:
        for tile in self.tiles:
            painter.setBrush(QBrush(tile.color))
            painter.drawPath(tile.path)

    def paint_pieces(self, painter):

        # for tile in [t for t in Board.TILES if t.piece is not None]:
        for tile in [t for t in self.tiles if t.piece is not None]:
            if tile.piece.player == 'B':
                painter.setBrush(QBrush(Qt.black))
                painter.setPen(QPen(Qt.black, 0.1 * self.r_hex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.white))
                pen = QPen(Qt.white, 0.12 * sqrt(3) * self.r_hex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

            elif tile.piece.player == 'W':
                painter.setBrush(QBrush(Qt.white))
                painter.setPen(QPen(Qt.black, 0.1 * self.r_hex))
                painter.drawPath(self.piece_circle_path(tile))

                painter.setBrush(QBrush(Qt.black))
                pen = QPen(Qt.black, 0.12 * sqrt(3) * self.r_hex)
                pen.setCapStyle(Qt.RoundCap)
                painter.setPen(pen)
                painter.drawPath(self.piece_sign_path(tile))

    def paint_names(self, painter):
        painter.setPen(QPen(Qt.red))
        text_font = QFont()
        text_font.setPointSize(10)
        text_font.setBold(True)
        painter.setFont(text_font)

        for tile in self.tiles:
            c = tile.pos
            r = QRectF(c.x() - self.r_hex, c.y() - self.r_hex, self.r_hex * 2, sqrt(3) * self.r_hex)
            coord_text = " {}\n({},{})".format(tile.name, tile.coord.x(), tile.coord.y())
            painter.drawText(r, Qt.AlignCenter, coord_text)

    def paint_buttons(self, painter):
        painter.setBrush(Qt.white)
        painter.setPen(QPen(Qt.black, 4))

        painter.drawEllipse(QPoint(self.contentsRect().width() - 50, self.contentsRect().height() - 50), 35, 35)
        painter.drawText(QRectF(self.contentsRect().width() - 80, self.contentsRect().height() - 80, 60, 60),
                         Qt.AlignCenter, "MOVE\nWHITE")

        painter.setBrush(Qt.black)
        painter.setPen(QPen(Qt.white, 4))

        painter.drawEllipse(QPoint(self.contentsRect().width() - 50, 50), 35, 35)
        painter.drawText(QRectF(self.contentsRect().width() - 80, 20, 60, 60),
                         Qt.AlignCenter, "MOVE\nBLACK")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.fillRect(self.contentsRect(), Qt.lightGray)

        self.paint_tiles(painter)
        self.paint_pieces(painter)
        self.paint_names(painter)
        self.paint_buttons(painter)

        painter.setPen(QPen(Qt.black, 8))
        font = QFont()
        font.setPointSize(20)
        painter.setFont(font)
        if get_player() == "W":
            painter.setPen(QPen(Qt.white, 8))
        painter.drawText(QRectF(10, 10, 60, 60), Qt.AlignCenter, get_player())
    # endregion

    def move_piece(self, _from, _to):
        self.tiles = move_piece(_from, _to, self.tiles)
        self.update()

    # region Mouseclick Functions
    def tile_at(self, mouse_pos):
        for i, tile in enumerate(self.tiles):
            if tile.path.contains(mouse_pos):
                return tile
        return -1

    def button_at(self, mouse_pos):
        white_button = QPainterPath()
        white_button.addEllipse(QPointF(self.contentsRect().width() - 50, self.contentsRect().height() - 50), 35, 35)
        if white_button.contains(mouse_pos):
            return True, "W"

        black_button = QPainterPath()
        black_button.addEllipse(QPointF(self.contentsRect().width() - 50, 50), 35, 35)
        if black_button.contains(mouse_pos):
            return True, "B"

        return False, ""

    def mousePressEvent(self, event):

        mouse_pos = event.pos()
        tile_clicked = self.tile_at(mouse_pos)
        self.stack.push(self.tiles)

        global TREE

        if tile_clicked == -1:
            button_clicked, move_player = self.button_at(mouse_pos)
            if not button_clicked:
                print '\033[1;41m' + "TILE CLICKED NOT RECOGNIZED" + '\033[1;m'
                self.selected = None
                return
            elif move_player == "W":
                if get_player() == "B":
                    print '\033[1;46m' + "IT'S THE BLACK :PLAYER'S TURN" + '\033[1;m'
                else:
                    #self.stack.push(self.tiles)
                    self.expand_root()
            elif move_player == "B":
                if get_player() == "W":
                    print '\033[1;46m' + "IT'S THE WHITE PLAYER'S TURN" + '\033[1;m'
                else:
                    #self.stack.push(self.tiles)
                    self.expand_root()
            self.selected = None
            return


        if self.selected is not None:
            if tile_clicked.piece is None:




                parent_hash = TT.get_zhash(self.tiles)
                print "From board with hash ", parent_hash

                set_player(get_opponent())
                self.update()

                print "Move to ", tile_clicked.name
                self.tiles = move_piece(self.selected, tile_clicked, self.tiles, False)
                print "new hash:", TT.get_zhash(list(self.tiles))
                TREE.add_node(self.tiles, parent_hash)

                TREE.write_tree("textfiles/tree.txt")

                self.stack.push(self.tiles)
                # self.stack.print_stack()
                self.selected = None
                return

        if tile_clicked.piece is None:
            print '\033[1;43m' + "NO PIECE ON TILE CLICKED" + '\033[1;m'
            self.selected = None
            return

        if tile_clicked.piece.player == get_opponent():
            if get_player() == "B":
                print '\033[1;46m' + "IT'S THE BLACK PLAYER'S TURN" + '\033[1;m'
            else:
                print '\033[1;46m' + "IT'S THE WHITE PLAYER'S TURN" + '\033[1;m'
            self.selected = None
            return

        if self.selected is None:
            self.selected = tile_clicked
            print "Selected ", self.selected.name



        self.update()
    # endregion

    def expand_root(self, initial_tile=None):

        move = Move(self.stack, initial_tile)
