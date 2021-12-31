import arcade
import math
from piece import Piece
from consts import COLS, ROWS, SIZE, OCCUPIED


class Board:
    def __init__(self):
        self.grid = []
        self.all_moves = {}
        self.capture_moves = {}

    def new_board(self, playerA, playerB):
        # make empty board
        self.grid = [[0] * ROWS for _ in range(COLS)]
        # add pieces in initial positions
        for i in range(COLS):
            for j in range(ROWS):
                if self._is_square_even(i, j):
                    if j < OCCUPIED:
                        self.grid[i][j] = Piece(i, j, playerA, 1)
                    elif j > ROWS - OCCUPIED - 1:
                        self.grid[i][j] = Piece(i, j, playerB, -1)

    def _is_square_even(self, col, row):
        return (col + row) % 2 == 0

    def get_pos(self, x, y):
        col = x // SIZE
        row = y // SIZE
        return col, row

    def get_piece(self, col, row):
        return self.grid[col][row]

    def move_piece(self, piece, col, row):
        # set piece to new position
        target = (col, row)
        self.grid[piece.col][piece.row] = 0
        self.grid[col][row] = piece
        captured = self.all_moves[(piece.col, piece.row)][target]
        piece.move(col, row)

        # gnererate new moves if multi-jump possible
        self.all_moves = {}
        self.capture_moves = {}
        if captured:
            self.grid[captured.col][captured.row] = 0
            all_dict, capture_dict = self._get_moves_for_piece(piece)
            if capture_dict:
                self.all_moves[target] = all_dict
                self.capture_moves[target] = capture_dict

        # check if piece reached end
        if row == ROWS - 1 or row == 0:
            piece.make_king()

    def generate_moves(self, player):
        self.all_moves = {}
        self.capture_moves = {}
        for i in range(COLS):
            for j in range(ROWS):
                piece = self.grid[i][j]
                if piece != 0 and piece.val == player:
                    all_dict, capture_dict = self._get_moves_for_piece(piece)
                    pos = (piece.col, piece.row)
                    if all_dict:
                        self.all_moves[pos] = all_dict
                    if capture_dict:
                        self.capture_moves[pos] = capture_dict

    def _get_moves_for_piece(self, piece):
        all_dict = {}
        capture_dict = {}
        # check "forwards"
        self._append_move(piece.col, piece.row, piece.dir, 1, all_dict, capture_dict)
        self._append_move(piece.col, piece.row, piece.dir, -1, all_dict, capture_dict)

        if piece.is_king():
            # check "backwards"
            self._append_move(
                piece.col, piece.row, -piece.dir, 1, all_dict, capture_dict
            )
            self._append_move(
                piece.col, piece.row, -piece.dir, -1, all_dict, capture_dict
            )

        return all_dict, capture_dict

    def _append_move(self, col, row, vertical, horizontal, all_dict, capture_dict):
        target = None
        captured = None
        c = col
        # analyse next two diagonal squares
        for r in range(row + vertical, row + vertical * 3, vertical):
            c += horizontal
            # out of bounds check
            if c < 0 or c > COLS - 1:
                break
            if r < 0 or r > ROWS - 1:
                break

            # check target square
            piece = self.grid[c][r]
            if piece == 0:
                target = (c, r)
                break
            elif piece.val == self.grid[col][row].val:
                break
            else:
                captured = piece

        # append to dictionary
        if target:
            all_dict[target] = captured  # None or captured piece
            if captured:
                capture_dict[target] = captured

    def is_move_valid(self, piece, col, row):
        pos = (piece.col, piece.row)
        target = (col, row)

        if self.must_capture():
            return pos in self.capture_moves and target in self.capture_moves[pos]
        else:
            return pos in self.all_moves and target in self.all_moves[pos]

    def must_play_piece(self, col, row):
        pos = (col, row)
        if self.must_capture():
            return pos in self.capture_moves
        else:
            return pos in self.all_moves

    def can_move(self):
        return bool(self.all_moves)

    def must_capture(self):
        return bool(self.capture_moves)

    def draw_grid(self):
        arcade.set_background_color(arcade.color.BEIGE)
        for i in range(COLS):
            for j in range(ROWS):
                if self._is_square_even(i, j):
                    x = SIZE * i
                    y = SIZE * j
                    arcade.draw_lrtb_rectangle_filled(
                        x, x + SIZE, y + SIZE, y, arcade.csscolor.SADDLE_BROWN
                    )

    def draw_moves(self, piece):
        pos = (piece.col, piece.row)
        moves = self.capture_moves if pos in self.capture_moves else self.all_moves

        for (col, row) in moves[pos]:
            x = SIZE * col
            y = SIZE * row
            outline = math.ceil(SIZE * 0.05)
            arcade.draw_lrtb_rectangle_outline(
                x, x + SIZE, y + SIZE, y, arcade.csscolor.RED, outline
            )

    def draw_pieces(self, exclusion):
        for i in range(COLS):
            for j in range(ROWS):
                piece = self.grid[i][j]
                if piece != 0 and piece != exclusion:
                    piece.draw()
