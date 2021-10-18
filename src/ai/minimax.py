import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm

        return best_movement

import random
from copy import deepcopy
from time import time

from src.utility import *
from src.model import State

from typing import Tuple, List


class MinimaxBagus:
    def __init__(self):
        pass

    def check_n_streak(self, board: Board, row: int, col: int, shape: str, color: str):
        piece = board[row, col]
        shape_streak = 0
        color_streak = 0
        streak_way = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for row_ax, col_ax in streak_way:
            row_ = row + row_ax
            col_ = col + col_ax

            temp_color_streak = 0
            temp_shape_streak = 0
            for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                if is_out(board, row_, col_):
                    break
                
                if piece.shape == board[row_, col_].shape:
                    temp_shape_streak += 1
                if piece.color == board[row_, col_].color:
                    temp_color_streak += 1
            shape_streak += (temp_shape_streak ** 2)
            color_streak += (temp_color_streak ** 2)

        return shape_streak, color_streak

    def count_streak(self, board: Board, shape: str, color: str):
        shape_streak = 0
        color_streak = 0
        for row in range(board.row):
            for col in range(board.col):
                streak_count_shape, streak_count_color = self.check_n_streak(board, row, col, shape, color)
                shape_streak += streak_count_shape
                color_streak += streak_count_color
        return shape_streak, color_streak

    def utility(self, state: State):
        winner = is_win(state.board)
        player = state.players[self.n_player]
        enemy = state.players[self.other_player]

        if winner != None:
            if winner[0] == player.shape and winner[1] == player.color:
                return 100
            else:
                return -100

        player_streak = sum(self.count_streak(state.board, player.shape, player.color))
        enemy_streak = sum(self.count_streak(state.board, enemy.shape, enemy.color))

        score = player_streak - enemy_streak
        if score == 0:
            score = random.uniform(0, 2)

        return score

    def terminate_condition(self, state: State):
        if is_win(state.board) or is_full(state.board):
            return True
        return False

    def gen_possible_moves(self, state: State, cur_player: int):
        quota = state.players[cur_player].quota
        possible_moves = []
        for k, v in quota.items():
            if v == 0:
                continue
            for i in range(state.board.col):
                possible_moves.append((i, k))
        return possible_moves

    def minimax(
        self,
        is_max: bool,
        possible_moves: List[int],
        state: State,
        depth: int,
        alpha: float = float("-inf"),
        beta: float = float("inf"),
        expected_path: List[State] = [],
    ) -> float:

        if depth == 0 or self.terminate_condition(state):
            return expected_path, self.utility(state)

        if is_max:
            best_val = float("-inf")
            best_path = None
            for move in possible_moves:
                temp_state = deepcopy(state)
                mark = place(temp_state, self.n_player, move[1], move[0])
                if mark != -1:
                    temp_path = deepcopy(expected_path)
                    temp_path.append((move, temp_state))
                    path, val = self.minimax(
                        not (is_max),
                        self.gen_possible_moves(state, self.other_player),
                        temp_state,
                        depth - 1,
                        alpha,
                        beta,
                        temp_path,
                    )

                    if val > best_val:
                        best_path = path
                        best_val = val

                    if time() > self.thinking_time:
                        return best_path, best_val
                    
                    alpha = max(best_val, alpha)
                    if beta <= alpha:
                        break
            return best_path, best_val

        else:
            best_val = float("inf")
            best_path = None
            for move in possible_moves:
                temp_state = deepcopy(state)
                mark = place(temp_state, self.other_player, move[1], move[0])
                if mark != -1:
                    temp_path = deepcopy(expected_path)
                    temp_path.append((move, temp_state))
                    path, val = self.minimax(
                        not (is_max),
                        self.gen_possible_moves(state, self.n_player),
                        temp_state,
                        depth - 1,
                        alpha,
                        beta,
                        temp_path,
                    )

                    if val < best_val:
                        best_path = path
                        best_val = val

                    if time() > self.thinking_time:
                        return best_path, best_val

                    beta = min(best_val, beta)
                    if beta <= alpha:
                        break
            return best_path, best_val

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[int, int]:
        self.thinking_time = time() + thinking_time
        self.n_player = n_player
        if n_player == 0:
            self.other_player = 1
        else:
            self.other_player = 0

        self.best_move = None

        path, val = self.minimax(
            True, self.gen_possible_moves(state, self.n_player), state, 3
        )

        return path[0][0]
