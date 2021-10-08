from math import inf
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

    def action(state):
        # kumpulan action yang bisa dilakuin
        pass

    def results(s, a):
        pass

    def terminal_test(state):
        # check udah menang atau belom
        pass

    def utility(state):
        # hasil nilainya kalau udah menang
        pass

    def max_value(state):
        if terminal_test(state):
            return utility(state)
        v = -999999
        for item in action(state):
            v = max(v, min_value(results(state, item)))   

    def min_value(state):
        if terminal_test(state):
            return utility(state)
        v = 999999
        for item in action(state):
            v = max(v, max_value(results(state, item))) 
