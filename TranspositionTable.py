from Utilities import *
from random import *
seed(1)

class TranspositionTable:

    def __init__(self):
        n_pieces = 6           #Black/White Positron/Electron/Neutron
        n_tiles = 91

        black_n = 0
        black_p = 1
        black_e = 2
        white_n = 3
        white_p = 4
        white_e = 5

        self.z_array = [[[0] * 91] * 3] * 2
        for player in range(2):
            for piece in range(3):
                for tile in range(91):
                    self.z_array[player][piece][tile] = getrandbits(64)

        self.z_black_move = getrandbits(64)

    def get_zhash(self, board):# black_n, black_p, black_e, white_n, white_p, white_e):

        piece_pos = self.get_piece_pos(board)
        for p in piece_pos:
            print p

        return_zkey = 0
        for i in range(91):
            if ((piece_pos[0] >> i) & 1):
                return_zkey ^= self.z_array[0][0][i]
            elif ((piece_pos[3] >> i) & 1):
                return_zkey ^= self.z_array[1][0][i]
            for bp in piece_pos[1]:
                if ((bp >> i) & 1):
                    return_zkey ^= self.z_array[0][1][i]
                    continue
            for wp in piece_pos[4]:
                if ((wp >> i) & 1):
                    return_zkey ^= self.z_array[1][1][i]
                    continue
            for be in piece_pos[2]:
                if ((be >> i) & 1):
                    return_zkey ^= self.z_array[0][2][i]
                    continue
            for we in piece_pos[5]:
                if ((we >> i) & 1):
                    return_zkey ^= self.z_array[1][2][i]
                    continue

        if get_player() == "B":
            return_zkey ^= self.z_black_move

        return return_zkey

    def get_piece_pos(self, boardtiles):
        piece_pos = [0, [ ], [ ], 0, [ ], [ ]]
        for i, tile in enumerate(boardtiles):
            if isinstance(tile.piece, PieceItem):
                if tile.piece.name == "BN":
                    piece_pos[0] = i
                elif tile.piece.name == "WN":
                    piece_pos[3] = i
                elif tile.piece.name[:2] =="BP":
                    piece_pos[1].append(i)
                elif tile.piece.name[:2] == "BE":
                    piece_pos[2].append(i)
                elif tile.piece.name[:2] == "WP":
                    piece_pos[4].append(i)
                elif tile.piece.name[:2] == "WE":
                    piece_pos[5].append(i)

        return piece_pos

TT = TranspositionTable()