from Utilities import *
from random import *
seed(1)


class TranspositionTable:

    def __init__(self):
        n_tiles = 91
        n_piece_types = 3   #Neutron, Positron, Electron

        '''black_n = 0
        black_p = 1
        black_e = 2
        white_n = 3
        white_p = 4
        white_e = 5'''

        #z_array[player][piece_type][tile]
        self.z_array = [[[0] * n_tiles] * n_piece_types] * 2
        for player in range(2):
            for piece in range(n_piece_types):
                for tile in range(n_tiles):
                    self.z_array[player][piece][tile] = getrandbits(64)

        # Whether it's black's turn to move
        self.z_black_move = getrandbits(64)

    def empty_tile(self, tile, piece_pos):
        for p in piece_pos:
            if tile in p:
                return False
        return True

    def get_zhash(self, board):

        piece_pos = self.get_piece_pos(board)

        # the subarrays with black/white positron/electrons are (reverse( sorted on length such that the for-loop runs
        # optimally --> if there are more values in the subarray, the probability of having a piece in a tile is higher
        sorted_piece_pos = sorted(piece_pos[2:], key=len)[::-1]

        return_zkey = 0
        for i in range(91):

            if self.empty_tile(i, piece_pos):
                # print(i, "empty")
                continue
            # print(i, "nonempty")
            found = False

            # Checking if piece contains black/white positron/electron
            for spp in sorted_piece_pos:
                if i in spp:
                    orig_index = piece_pos.index(spp)
                    if orig_index % 2 == 0:
                        # print(i, orig_index, int(orig_index / 2))
                        return_zkey ^= self.z_array[0][int(orig_index / 2)][i]
                    else:
                        # print(i, orig_index, int(orig_index / 2))
                        return_zkey ^= self.z_array[1][int(orig_index / 2)][i]
                    found = True
                    break
            if found:
                continue

            # If no black/white positron/electron, check for black/white neuron
            # Checked last as probability is smallest: only 1 black and 1 white neutron
            if i == piece_pos[0][0]:
                # print(i, 0)
                return_zkey ^= self.z_array[0][0][i]

            elif i == piece_pos[1][0]:
                # print(i, 0)
                return_zkey ^= self.z_array[1][0][i]

        if get_player() == "B":
            print "Black to move next"
            return_zkey ^= self.z_black_move
        else:
            print "White to move next"

        return return_zkey

    def get_piece_pos(self, board_tiles):
        piece_pos = [[], [], [], [], [], []]
        for i, tile in enumerate(board_tiles):
            if isinstance(tile.piece, PieceItem):
                if tile.piece.name[:2] == "BP":
                    piece_pos[2].append(i)
                elif tile.piece.name[:2] == "BE":
                    piece_pos[4].append(i)
                elif tile.piece.name[:2] == "WP":
                    piece_pos[3].append(i)
                elif tile.piece.name[:2] == "WE":
                    piece_pos[5].append(i)
                elif tile.piece.name == "BN":
                    piece_pos[0] = [i]
                elif tile.piece.name == "WN":
                    piece_pos[1] = [i]

        return piece_pos

TT = TranspositionTable()