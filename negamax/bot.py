import time
import math
import random
from copy import deepcopy
from negamax.table import Table
from consts import COLS, ROWS


class Bot:
    def __init__(self, val):
        self.val = val
        self.counter = 0
        self.table = Table()

    def has_turn(self, player):
        return self.val == player

    def make_move(self, game, max_time):
        t_0 = time.time()
        d_t = 0
        depth = 0
        self.counter = 0
        score = 0
        moves = []

        move = self._forced_move(game.board)
        if move:
            # only a single move possible
            moves = [move]
        else:
            # iterative deepening with negamax
            while d_t < max_time and abs(score) != math.inf:
                self.table.clear()
                depth += 1
                score, moves = self._negamax(
                    game.board, game.current, game.next, depth, -math.inf, math.inf
                )
                d_t = time.time() - t_0

        print("execution time", d_t)
        print("game tree depth", depth)
        print("explored states", self.counter)
        print("expected score", score)
        print("best move(s)", moves)

        (pos, target) = random.choice(moves)
        piece = game.board.get_piece(*pos)
        game.make_move(piece, *target)

    def _negamax(self, board, current, next, depth, alpha, beta):
        a = alpha

        # look up board state in transposition table
        hash_code = self.table.hash_board(board, self.val)
        entry, bound = self.table.get_entry(hash_code)
        if entry:
            if bound == Table.EXACT:
                return entry, []
            elif bound == Table.LOWER:
                alpha = max(alpha, entry)
            elif bound == Table.UPPER:
                beta = min(beta, entry)

            if alpha >= beta:
                return entry, []

        self.counter += 1

        # terminal nodes
        if not board.can_move() and not board.must_capture():  # game over
            if current == self.val:  # game is won
                return math.inf, []
            else:  # game is lost
                return -math.inf, []
        if depth == 0:  # leaf node
            return self._evaluate(board, current, next), []

        # recursive step
        max_score = -math.inf
        best_moves = []
        options = board.capture_moves if board.must_capture() else board.all_moves

        for pos in options:
            for target in options[pos]:
                move = (pos, target)
                next_board = self._simulate_move(board, pos, target)

                if next_board.must_capture():
                    # simulate a multi-jump
                    score, _ = self._negamax(
                        next_board, current, next, depth, alpha, beta
                    )
                else:
                    next_board.generate_moves(next)
                    score, _ = self._negamax(
                        next_board, next, current, depth - 1, -beta, -alpha
                    )
                    score *= -1

                if score >= max_score:
                    if score == max_score:
                        best_moves.append(move)
                    else:
                        best_moves = [move]
                    max_score = score

                alpha = max(alpha, score)
                if alpha >= beta:
                    break

        if max_score <= a:
            self.table.set_entry(hash_code, max_score, Table.UPPER)
        elif max_score >= beta:
            self.table.set_entry(hash_code, max_score, Table.LOWER)
        else:
            self.table.set_entry(hash_code, max_score, Table.EXACT)

        return max_score, best_moves

    def _forced_move(self, board):
        if len(board.capture_moves) == 1:
            (pos, targets) = next(iter(board.capture_moves.items()))
            if len(targets) == 1:
                (target, _) = next(iter(board.capture_moves[pos].items()))
                return (pos, target)

        return None

    def _evaluate(self, board, playerA, playerB):
        sum_pawns_A, sum_kings_A = self._count(board, playerA)
        sum_pawns_B, sum_kings_B = self._count(board, playerB)

        return sum_pawns_A + 2 * sum_kings_A - (sum_pawns_B + 2 * sum_kings_B)

    def _count(self, board, player):
        sum_pawns = 0
        sum_kings = 0
        for i in range(COLS):
            for j in range(ROWS):
                piece = board.get_piece(i, j)
                if piece != 0 and piece.val == player:
                    if piece.is_king():
                        sum_kings += 1
                    else:
                        sum_pawns += 1

        return sum_pawns, sum_kings

    def _simulate_move(self, board, pos, target):
        board = deepcopy(board)
        piece = board.get_piece(*pos)
        board.move_piece(piece, *target)
        return board
