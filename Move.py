from PyQt4.QtCore import QObject
from Utilities import *
from Board import *
from BoardTree import *
from PhwarMain import TT

DEPTH = 1
# CURRENT_PLAYER = "B"
# if get_opponent() == "B":
#    CURRENT_PLAYER = "W"
# BOARD_BEFORE_ANYTHING = list()

class Move(QObject):

    # execute_best_move = pyqtSignal(list)
    # send_color = pyqtSignal(list)

    # +++ NEW ++++++++++++++++++++
    # made_move = pyqtSignal(tuple)

    ply_counter = 0

    def __init__(self, boardstack, initial_tile=None):

        self.print_boards = True         # Set to True is all board in the stack should be printed
        self.print_move_values = True    # Set to True if all the values for the moves should be printed

        super(Move, self).__init__()
        self.boardstack = boardstack
        self.visited = BoardStack()

        self.tiles = list(boardstack.peek())
        self.visited.push(self.tiles)
        #self.filename = filename

        self.center_tile = filter(lambda x: x.coord == QPoint(get_board_size()[0] - 1,
                                                              get_board_size()[1] / 2), self.tiles)[0]

        self.moves_so_far = list()
        self.pieces_on_board = filter(lambda x: x.piece.player == get_player(),
                                      filter(lambda y: y.piece is not None, self.tiles))


        max_move_value = -float('inf')
        max_moves = list()
        for piece in self.pieces_on_board:
            move_result_values = self.find_moves(piece)
            for _from, _to, _v in move_result_values:
                if _v >= max_move_value:
                    max_moves.append((_from, _to))
                    max_move_value = _v

                if self.print_move_values:
                    print "{:<40}{:>10}".format("RESULT VALUE OF {} MOVING TO {}:".format(_from.name, _to.name),_v)

            xxx = 0
        Move.ply_counter += 1

    def find_moves(self, initial_tile):
        move_values = list()
        self.tiles = self.boardstack.peek()

        for moved_to_tile in find_free_tiles(initial_tile, find_line_of_sight(initial_tile, self.tiles)):

            move_value = 0

            # writing the tile to move on output
            # printer_str = " Found Move From {} to {} ".format(initial_tile.name, moved_to_tile.name)
            # printer_str = "\n{:+^40}".format(printer_str)

            # print printer_str
            # writing it to results.txt
            # file = open(self.filename, "a")
            # file.write("\n" + printer_str + "\n")
            # file.close()

            global TT, TREE
            print "fom move parent_hash: ", TT.get_zhash(self.tiles)
            tiles = move_piece(initial_tile, moved_to_tile, self.tiles)

            TREE.add_node(tiles, TT.get_zhash(self.tiles))

            self.boardstack.push(tiles)
            #self.visited.push(tiles)
            if self.print_boards:
                print "\n", initial_tile.name, " --> ", moved_to_tile.name
                self.boardstack.print_stack()

            # Writing the board with the piece moved to the new tile to boards.txt
            # file = open("boards.txt", "a")
            # file = open("boards.log", "a")
            # file.write("\n{:^65}\n".format("BOARD DUE TO MOVEMENT {} TO {}".format(initial_tile.name, moved_to_tile.name)))
            # file.write(print_hex(tiles))
            # file.close()

            # print "\n{:^65}\n".format("BOARD DUE TO MOVEMENT {} TO {}".format(initial_tile.name, moved_to_tile.name))
            # print print_hex(tiles)

            '''size_stack_before_captures = self.boardstack.size()
            tile_captured, capture_value = self.capture_found(moved_to_tile)
            move_value += capture_value

            while self.boardstack.size() > size_stack_before_captures:
                tile_captured, capture_value = self.capture_found(tile_captured)
                move_value += capture_value

                if Move.ply_counter < 2 * DEPTH:
                    if capture_value == 0:
                        print "SWITCHING PLAYER FROM {} TO {}".format(get_player(), get_opponent())
                        switch_player()
                        ply2 = Move(self.boardstack)
                self.boardstack.pop()

            self.boardstack.pop()
            move_values.append((initial_tile, moved_to_tile, move_value))'''

        return move_values

    def capture_found(self, moved_tile):
        tiles = list(self.boardstack.peek())
        new_sight = find_line_of_sight(moved_tile, tiles)

        #opp_pieces = filter(lambda x: x.piece.player == get_opponent(), filter(lambda y: y.piece is not None, tiles))
        #opp_pieces = filter(lambda x: find_pieces_in_sight(x, find_line_of_sight(x, tiles), get_player()).__len__() > 1,
        #                                   opp_pieces)
        #for pp in opp_pieces:
        #    print pp.name

        '''for opp_p in opp_pieces:
            opp_lines_of_sight = find_line_of_sight(opp_p, tiles)
            sight_attackers = find_pieces_in_sight(opp_p, opp_lines_of_sight, get_player())
            print opp_p.name
            for _s in sight_attackers:
                print _s.name

            print sum(1 for p in sight_attackers if p.piece.player == get_player())
            xxxxx = 0'''
        opp_pieces = find_pieces_in_sight(moved_tile, new_sight, get_opponent())

        if opp_pieces.__len__() == 0:
            return moved_tile, 0

        else:
            for opp_piece in opp_pieces:
                attackers, c, t = self.capture(opp_piece, tiles)
                if t == 0 and c >= 2:
                    value = self.capture_value(opp_piece, tiles)
                    for attacker in attackers:
                        tiles_after_capture = list(move_piece(attacker, opp_piece, tiles, True))
                        if not self.visited.push(tiles_after_capture):
                            print "already visited"
                            print print_hex(tiles_after_capture)
                            print print_hex(self.visited.peek())
                            continue

                        self.boardstack.push(tiles_after_capture)
                        #self.visited.push(tiles_after_capture)

                        if self.print_boards:
                            print "\n{:^65}\n".format(
                                "BOARD DUE TO CAPTURE MOVEMENT {} TO {} (VALUE: {})".format(attacker.name,
                                                                                            opp_piece.name,
                                                                                            value))
                            self.boardstack.print_stack()
                        # printer_str = " Found Capture Of {} By {} ".format(opp_piece.name, attacker.name)
                        # file = open("boards.txt", "a")
                        # file = open("boards.log", "a")
                        # file.write("\n{:^65}\n".format(printer_str))
                        # file.write("\n{:^65}\n".format(
                        #    "BOARD DUE TO MOVEMENT {} TO {}".format(attacker.name, opp_piece.name)))
                        #file.close()
                        #printer_str = " {:+^38} ".format(printer_str)
                        #print printer_str
                        #file = open("boards.txt", "a")
                        # file.write(print_hex(tiles_after_capture))
                        # file.close()
                        # print print_hex(tiles_after_capture)

                    return opp_piece, self.capture_value(opp_piece, tiles)
            return moved_tile, 0

    def capture(self, piece, tiles):

        total_loading = 0
        counter = 0
        attacking_pieces = list()

        opp_sight = find_line_of_sight(piece, tiles)
        pieces_in_sight = find_pieces_in_sight(piece, opp_sight)
        printer = "pieces in sight to check capture of {}, {}: ".format(piece.name, piece.piece.name)
        for p in pieces_in_sight:

            printer += "(" + p.name + " , " + p.piece.name + ") "

            if p.piece.player == get_player():
                counter += 1
                attacking_pieces.append(p)

            if p.piece.sign == "P":
                total_loading += 1
            elif p.piece.sign == "E":
                total_loading -= 1

        #print printer
        if counter >= 2 and total_loading == 0:
            return attacking_pieces, counter, total_loading

        # TODO: retrun False
        return False, False, False
        # return list(), counter, total_loading

    def capture_value(self, capt, tiles):

        if capt.piece.sign == "N":
            return float('inf')

        positrons = 0
        electrons = 0
        for tiles in filter(lambda x: x.piece.player == capt.piece.player,
                                filter(lambda y: isinstance(y.piece, PieceItem), tiles)):
            if tiles.piece.sign == "P":
                positrons += 1
            if tiles.piece.sign == "E":
                electrons += 1

        if capt.piece.sign == "P":
            if positrons == 1:
                return float('inf')
            return 5 - positrons
        if capt.piece.sign == "E":
            if electrons == 1:
                return float('inf')
            return 5 - electrons