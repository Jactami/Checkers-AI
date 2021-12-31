import arcade
from game import Game
from negamax.bot import Bot
from consts import WIDTH, HEIGHT


class Main(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Checkers")

    def setup(self):
        self.game = Game()
        self.bot = Bot(self.game.current)

    def draw(self):
        arcade.start_render()
        self.game.draw()
        arcade.finish_render()

    def on_mouse_press(self, x, y, button, modifiers):
        self.game.select_piece(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.game.drag_piece(dx, dy)

    def on_mouse_release(self, x, y, button, modifiers):
        self.game.drop_piece(x, y)

    def on_key_press(self, symbol, modifiers):
        if self.game.winner:
            self.game.new_game()

    def on_show(self):
        self.draw()

    def on_draw(self):
        pass

    def on_update(self, delta_time):
        self.draw()

        if self.game.winner:
            return

        if self.bot.has_turn(self.game.current):
            self.bot.make_move(self.game, 1)


if __name__ == "__main__":
    window = Main()
    window.setup()
    arcade.run()
