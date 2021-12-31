import arcade
from board import Board
from arcade.color import WHITE


class Game:
    def __init__(self):
        self.board = Board()
        self.new_game()

    def new_game(self):
        self.current = arcade.csscolor.BLACK
        self.next = arcade.csscolor.WHITE
        self.winner = None
        self.board.new_board(self.current, self.next)
        self.board.generate_moves(self.current)
        self.selected = None
        self.counter = 1
        print("New game started.")

    def select_piece(self, x, y):
        if self.selected:
            return

        col, row = self.board.get_pos(x, y)
        piece = self.board.get_piece(col, row)

        if self._is_selection_valid(piece):
            self.selected = piece

    def drag_piece(self, dx, dy):
        if not self.selected:
            return

        self.selected.drag(dx, dy)

    def drop_piece(self, x, y):
        if not self.selected:
            return

        col, row = self.board.get_pos(x, y)
        self.make_move(self.selected, col, row)
        self.selected = None

    def make_move(self, piece, col, row):
        pos = (piece.col, piece.row)
        target = (col, row)
        if not self.board.is_move_valid(piece, col, row):
            # reset piece to previous position
            piece.move(piece.col, piece.row)
        else:
            self.board.move_piece(piece, col, row)
            print("Turn " + str(self.counter) + ": " + str(pos) + " to " + str(target))
            # continue if no multi-jump possible
            if not self.board.must_capture():
                self.board.generate_moves(self.next)
                # check if game is over
                if self.is_game_over():
                    self.winner = self.current
                    print("Game over. Press any key for new game.")
                else:
                    # change turns
                    self.current, self.next = self.next, self.current
                    self.counter += 1

    def _is_selection_valid(self, piece):
        if piece == 0 or piece.val != self.current:
            return False

        return self.board.must_play_piece(piece.col, piece.row)

    def is_game_over(self):
        # player can not move anymore or has no piece, e.g. has no possible moves
        return not self.board.can_move() and not self.board.must_capture()

    def draw(self):
        self.board.draw_grid()
        self.board.draw_pieces(self.selected)
        if self.selected:
            self.board.draw_moves(self.selected)
            self.selected.draw()
