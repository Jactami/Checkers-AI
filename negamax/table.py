import random
from consts import COLS, ROWS


class Table:

    EXACT = 0
    LOWER = 1
    UPPER = 2

    def __init__(self):
        self.cache = {}
        self._init_zobrist()

    def _init_zobrist(self):
        self.zobrist = []
        for i in range(COLS):
            self.zobrist.append([])
            for j in range(ROWS):
                self.zobrist[i].append([])
                for _ in range(4):
                    self.zobrist[i][j].append(random.getrandbits(128))

    def hash_board(self, board, player):
        hash_code = 0
        for i in range(COLS):
            for j in range(ROWS):
                piece = board.get_piece(i, j)
                if piece == 0:
                    continue
                if piece.val == player:
                    if not piece.is_king():
                        hash_code ^= self.zobrist[i][j][0]
                    else:
                        hash_code ^= self.zobrist[i][j][1]
                else:
                    if not piece.is_king():
                        hash_code ^= self.zobrist[i][j][2]
                    else:
                        hash_code ^= self.zobrist[i][j][3]

        return hash_code

    def clear(self):
        self.cache = {}

    def set_entry(self, key, value, bound):
        self.cache[key] = value, bound

    def get_entry(self, key):
        if key in self.cache:
            return self.cache[key]

        return None, None
