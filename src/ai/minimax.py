from math import inf
import random
import copy
from time import time

from src.constant import ShapeConstant
from src.constant import ColorConstant
from src.model import State
from src.model import Piece
from src.utility import place

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_movement = minimax(state, n_player)

        return best_movement

    def actions(self, state, n_player):
        # kumpulan action yang bisa dilakuin
        actions = []
        for col in range(0, state.board.col):
            if(state.board[0, col].shape == ShapeConstant.BLANK):
                for shape in [ShapeConstant.CROSS, ShapeConstant.CIRCLE]:
                    if state.players[n_player].quota[shape] != 0:
                        actions.append(col, shape)

        return actions

    def results(self, state, n_player, action):

        copyState = copy.deepcopy(state)

        place(copyState, n_player, action[1], action[0])
        # for row in range(copyState.board.row - 1, -1, -1):
        #     if(copyState.board[row, action[0]].shape == ShapeConstant.BLANK):
        #         copyState.board[row, action[0]] = Piece(
        #             action[1], copyState.players[n_player].color)
        #         break

        return copyState

    def terminal_test(self, state: State):
        # check udah menang atau belom
        pass

    def utility(self, state: State):
        # hasil nilainya kalau udah menang
        pass

    def minimax(self, state, n_player):

        best_action = (random.randint(0, state.board.col), random.choice(
            [ShapeConstant.CROSS, ShapeConstant.CIRCLE]))

        value = -999999
        alpha = -999999
        beta = 999999
        for action in actions(state, n_player):
            minimum = min_value(results(state, action), n_player, alpha, beta)
            if(minimum > value):
                value = minimum
                best_action = action

        return best_action

    def max_value(self, state, n_player, alpha, beta):
        if terminal_test(state):
            return utility(state)

        value = -999999
        for action in actions(state, n_player):
            value = max(value, min_value(
                results(state, action), n_player, alpha, beta))
            alpha = max(alpha, value)
            if(alpha >= beta):
                break

        return value

    def min_value(self, state, n_player, alpha, beta):
        if terminal_test(state):
            return utility(state)

        value = 999999
        for action in actions(state, n_player):
            value = min(value, max_value(
                results(state, action), n_player, alpha, beta))
            beta = max(beta, value)
            if(alpha >= beta):
                break

        return value
