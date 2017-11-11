from PyQt4.QtCore import QPoint, QPointF
from PyQt4.QtGui import QPainterPath, QColor


# region Setters & getters PLAYER and OPPONENT
PLAYER = str()
OPPONENT = str()


def set_player(player):
    global PLAYER, OPPONENT
    PLAYER = player
    if PLAYER == "B":
        OPPONENT = "W"
    else:
        OPPONENT = "B"


def set_opponent(opponent):
    global PLAYER, OPPONENT
    OPPONENT = opponent
    if OPPONENT == "B":
        PLAYER = "W"
    else:
        PLAYER = "B"


def switch_player():
    global PLAYER, OPPONENT
    if PLAYER == "B":
        set_player("W")
    else:
        set_player("B")


def get_player():
    global PLAYER
    return PLAYER


def get_opponent():
    global OPPONENT
    return OPPONENT
# endregion


# region Setters & getters NR and NC
NR = int()
NC = int()


def set_board_size(r, c):
    global NR
    NR = r
    global NC
    NC = c


def get_board_size():
    global NC
    global NR
    return NR, NC


def get_board_rows():
    global NR
    return NR


def get_board_cols():
    global NC
    return NC
# endregion


# region TileItem
class TileItem(object):

    def __init__(self, tile_item=None):
        object.__init__(self)
        if tile_item is not None:
            self.name = tile_item.name
            self.coord = tile_item.coord
            self.path = tile_item.path
            self.pos = tile_item.pos
            self.color = tile_item.color
            self.piece = tile_item.piece
        else:
            self.name = str()
            self.coord = QPoint()
            self.path = QPainterPath()
            self.pos = QPointF()
            self.color = QColor()
            self.piece = None

    def set_name(self, name):
        self.name = name

    def set_coord(self, coord):
        self.coord = coord

    def set_pos(self, pos):
        self.pos = pos

    def set_path(self, path):
        self.path = path

    def set_color(self, color):
        self.color = color

    def set_piece(self, piece):
        self.piece = piece

    def name(self):
        return self.name

    def coord(self):
        return self.coord

    def pos(self):
        return self.pos

    def path(self):
        return self.path

    def color(self):
        return self.color

    def piece(self):
        return self.piece
# endregion


# region PieceItem
class PieceItem():

    def __init__(self, player=None, sign=None, number=None, name=None, pieceitem=None):
        if pieceitem is not None:
            self.player = pieceitem.player
            self.sign = pieceitem.sign
            self.number = pieceitem.number
            self.tile = pieceitem.tile
            self.name = pieceitem.name

        elif name is not None:
            self.player = name[0]
            self.sign = name[1]
            self.name = name
            if name.__len__() > 2:
                self.number = int(name[2])
            else:
                self.number = int()

        else:
            if player is not None:
                self.player = player
            else:
                self.player = str()

            if sign is not None:
                self.sign = sign
            else:
                self.sign = str()

            if number is not None:
                self.number = number
            else:
                self.number = int()

            if player is not None and sign is not None:
                if number is not None:
                    self.name = self.player + self.sign + str(self.number)
                else:
                    self.name = self.player + self.sign

    def set_player(self, player):
        self.player = player

    def set_sign(self, sign):
        self.sign = sign

    def set_number(self, number):
        self.number = number

    def set_tile(self, tile):
        self.tile = tile

    def set_name(self):
        self.name = self.player + self.sign + str(self.number)

    def player(self):
        return self.player

    def sign(self):
        return self.sign

    def number(self):
        return self.number

    def tile(self):
        return self.tile

    def name(self):
        return self.name
# endregion


def own_initial_pieces(tiles, news):
    printing = str()
    for tile in tiles:
        tile.set_piece(None)
    print printing

    for i in range(news.__len__()):
        ti = filter(lambda j: tiles[j].name == news[i][1], range(tiles.__len__()))[0]
        tiles[ti].set_piece(PieceItem(name=news[i][0]))


# region Move Functions
def move_validity(_from, _to, tiles):
    _tiles = list(tiles)
    if not find_free_tiles(_from, find_line_of_sight(_from, _tiles)).__contains__(_to):
        los = find_line_of_sight(_from, tiles)
        line = filter(lambda x: _from in x and _to in x, los)[0]
        for line_tiles in line:
            if line_tiles.name == "F6":
                return 0
        return False
    return True


def move_piece(_from, _to, tiles, capture=False):
    _tiles = list(tiles)
    valid = move_validity(_from, _to, _tiles)
    if valid == 0 and not capture:
        _to = filter(lambda x: x.name == "F6", tiles)[0]
        valid = True

    if valid or capture:
        piece = PieceItem(pieceitem=_from.piece)
        tile_from = TileItem(_from)
        tile_to = TileItem(_to)
        #if capture:
        #    print tile_from.name, tile_from.piece.name, tile_to.name
        tile_from.set_piece(None)
        tile_to.set_piece(piece)
        _tiles[_tiles.index(_to)] = tile_to
        _tiles[_tiles.index(_from)] = tile_from
        #if capture:
        #    print tile_from.name, tile_to.name, tile_to.piece.name

    return _tiles
# endregion


# region Search Functions
def find_line_of_sight(tile, tiles):

    if tiles is None:
        return

    v_sight = filter(lambda t: t.coord.y() == tile.coord.y(), tiles)
    lr_sight = filter(lambda t: t.coord.x() - t.coord.y() == tile.coord.x() - tile.coord.y(), tiles)
    rl_sight = filter(lambda t: t.coord.x() + t.coord.y() == tile.coord.x() + tile.coord.y(), tiles)
    rl_sight.reverse()

    return [v_sight, lr_sight, rl_sight]


def find_pieces_in_sight(piece, lines_of_sight, player=None):

    pieces_in_sight = list()

    for sight in lines_of_sight:
        if not sight.__contains__(piece):
            piece = filter(lambda x: x.name == piece.name, sight)[0]

        i = sight.index(piece) - 1

        while i > -1:
            if isinstance(sight[i].piece, PieceItem):
                if player is None:
                    pieces_in_sight.append(sight[i])
                elif sight[i].piece.player == player:
                    pieces_in_sight.append(sight[i])
                break
            i -= 1

        i = sight.index(piece) + 1
        while i < sight.__len__():
            if isinstance(sight[i].piece, PieceItem):
                if player is None:
                    pieces_in_sight.append(sight[i])
                elif sight[i].piece.player == player:
                    pieces_in_sight.append(sight[i])
                break
            i += 1

    return pieces_in_sight


def find_free_tiles(piece, lines_of_sight):
    global NR, NC
    tiles_to_move_to = list()

    for sight in lines_of_sight:
        if not sight.__contains__(piece):
            return

        index = sight.index(piece)
        i = index - 1
        while i > -1:
            if isinstance(sight[i].piece, PieceItem):
                break
            else:
                tiles_to_move_to.append(sight[i])
                if sight[i].coord.x() == NR - 1 and sight[i].coord.y() == NC/2:
                    break
            i -= 1

        i = index + 1
        while i < sight.__len__():
            if isinstance(sight[i].piece, PieceItem):
                break
            else:
                tiles_to_move_to.append(sight[i])
                if sight[i].coord.x() == NR - 1 and sight[i].coord.y() == NC / 2:
                    break
            i += 1

    return tiles_to_move_to


# TODO: start at the end and move towards the tile to avoid checking captures multiple times
def find_free_pieces_backwards(piece, lines_of_sight):
    global NR, NC
    tiles_to_move_to = list()
    sight_direction = list()

    for sight in lines_of_sight:
        if not sight.__contains__(piece):
            return

        index = sight.index(piece)
        i = index - 1
        while i > -1:
            if isinstance(sight[i].piece, PieceItem):
                break
            else:
                sight_direction.insert(0, sight[i])
                if sight[i].coord.x() == NR - 1 and sight[i].coord.y() == NC / 2:
                    break
            i -= 1

        tiles_to_move_to.extend(sight_direction)
        del sight_direction[:]

        i = index + 1
        while i < sight.__len__():
            if isinstance(sight[i].piece, PieceItem):
                break
            else:
                sight_direction.insert(0, sight[i])
                if sight[i].coord.x() == NR - 1 and sight[i].coord.y() == NC / 2:
                    break
            i += 1

        tiles_to_move_to.extend(sight_direction)
        del sight_direction[:]

    return tiles_to_move_to
# endregion


# region Print Functions
def piece_as_sign(piece_name):
    if piece_name == "BN":
        return "%"
    if piece_name[:2] == "BP":
        return "+"
    if piece_name[:2] == "BE":
        return "-"
    if piece_name[:2] == "WN":
        return "%%"
    if piece_name[:2] == "WP":
        return "++"
    if piece_name[:2] == "WE":
        return "--"

    return "ERROR"


def print_hex(tiles, colored=True):
    global NR, NC
    lines = [""] * (NR * 2 - 1)
    lines[0] = "{:^6}".format("") * 5
    lines[1] = "{:^6}".format("") * 4
    lines[2] = "{:^6}".format("") * 3
    lines[3] = "{:^6}".format("") * 2
    lines[4] = "{:^6}".format("")

    lines[6] = "{:^6}".format("")
    lines[8] = "{:^6}".format("")
    lines[10] = "{:^6}".format("")
    lines[12] = "{:^6}".format("")
    lines[14] = "{:^6}".format("")
    lines[16] = "{:^6}".format("")

    lines[17] = "{:^6}".format("") * 2
    lines[18] = "{:^6}".format("") * 3
    lines[19] = "{:^6}".format("") * 4
    lines[20] = "{:^6}".format("") * 5

    for i, t in enumerate(tiles):
        index = int(t.name[1:]) - 1
        alpha = ord(t.name[0])

        if t.piece is None:
            lines[2 * index + alpha % 2] += "{:^6}{:^6}".format(t.name, "")
        else:
            if t.piece.name[0] == "B":
                if colored:
                    lines[2 * index + alpha % 2] += '\x1b[1;31;40m' + "{:^6}".format(t.piece.name) + '\x1b[0m'
                else:

                    lines[2 * index + alpha % 2] += "{:^6}".format(piece_as_sign(t.piece.name))
                lines[2* index + alpha % 2] += "{:^6}".format("")
            else:
                if colored:
                    lines[2 * index + alpha % 2] += '\x1b[1;31;47m' + "{:^6}".format(t.piece.name) + '\x1b[0m'
                else:
                    lines[2 * index + alpha % 2] += "{:^6}".format(piece_as_sign(t.piece.name))
                lines[2* index + alpha % 2] += "{:^6}".format("")

    board_str = "{:*^65}".format("") + "\n"
    for l in lines:
        board_str += l + "\n"
    board_str += "{:*^65}".format("")

    return board_str
# endregion


