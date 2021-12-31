import arcade
from consts import SIZE


class Piece:
    def __init__(self, col, row, val, dir):
        self.col = self.row = self.x = self.y = 0
        self.move(col, row)
        self.val = val
        self.dir = dir
        self.king = False

    def __repr__(self):
        return str((self.val, (self.col, self.row), self.king))

    def move(self, col, row):
        self.col = col
        self.row = row
        self.x = (self.col + 0.5) * SIZE
        self.y = (self.row + 0.5) * SIZE

    def is_king(self):
        return self.king

    def make_king(self):
        self.king = True

    def drag(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, SIZE * 0.4 + 1, arcade.csscolor.BLACK)
        arcade.draw_circle_filled(self.x, self.y, SIZE * 0.4, self.val)

        if self.king:
            # inverse color
            color = tuple(x - y for x, y in zip((255, 255, 255), self.val))
            arcade.draw_circle_filled(self.x, self.y, SIZE * 0.2, color)
            arcade.draw_circle_filled(self.x, self.y, SIZE * 0.2 - 4, self.val)
