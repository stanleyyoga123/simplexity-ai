from constant import DirectionConstant, ShapeConstant
from model.state import State

class Heuristic:
    def __init__(self, state: State) -> None:
        # represents whether NE, E, SE, S directions have been calculated
        self.state = state
        self.directions = [
            [
                [
                    {
                        "NE": False,
                        "E": False,
                        "SE": False,
                        "S": False
                    } for _ in range(state.board.col)
                ] for _ in range(state.board.row)
            ] for _ in range(2)
        ]

    def count_player(self, i: int, j: int, player_choice: int, direction: str) -> int:
        """
        [DESC]
            Menghitung jumlah piece yang berurutan dari baris `i` dan kolom `j`
            ke arah `S`, `SE`, `E`, atau `NE` untuk pemain bernomor `player_choice`
        """
        board = self.state.board
        player = self.state.players[player_choice]

        if self.directions[player_choice][i][j][direction]: return 0

        # Three conditions to stop counting
        wall = False
        crash = False
        blank = False

        row = i; col = j
        increment = [0, 0]
        if (direction == "NE"): increment = DirectionConstant.NE
        elif (direction == "E"): increment = DirectionConstant.E
        elif (direction == "SE"): increment = DirectionConstant.SE
        else: increment = DirectionConstant.S

        temp = 0
        while not (wall or crash or blank):
            if temp == 4:
                return 10000000

            if (row >= board.row) or (col >= board.col):
                wall = True
                continue
            piece = board.__getitem__((row, col))

            if piece.shape != player.shape and piece.color != player.color:
                crash = True
                continue

            if piece.shape == ShapeConstant.BLANK:
                blank = True
                continue

            temp += 1
            self.directions[player_choice][row][col][direction] = True
            row += increment[0]
            col += increment[1]

        if blank: return temp
        return 0

    def value(self, player_choice: int) -> int:
        """
        [PARAMS]
            player_choice: our player number
        """
        values = [0, 0]
        board = self.state.board

        opponent_choice = player_choice ^ 1
        for i in range(0, board.row, 1):
            for j in range(0, board.col, 1):
                values[player_choice] += self.count_player(i, j, player_choice, "S")
                values[player_choice] += self.count_player(i, j, player_choice, "SE")
                values[player_choice] += self.count_player(i, j, player_choice, "E")
                values[player_choice] += self.count_player(i, j, player_choice, "NE")

                values[opponent_choice] += self.count_player(i, j, opponent_choice, "S")
                values[opponent_choice] += self.count_player(i, j, opponent_choice, "SE")
                values[opponent_choice] += self.count_player(i, j, opponent_choice, "E")
                values[opponent_choice] += self.count_player(i, j, opponent_choice, "NE")

        return values[player_choice] - values[opponent_choice]
