# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot
#
# 1d numpy array board representation.
# Board Representation:
# 3 1 1 1 3    3 1 1 1 3
# 2 0 0 0 2     2 0 0 0 2
# 2 0 0 0 2 ==   2 0 0 0 2
# 2 0 0 0 2       2 0 0 0 2
# 3 1 1 1 3        3 1 1 1 3
# Where BORDER = 3, BLACK = 1, WHITE = 2, BLANK = 0


from copy import deepcopy
import numpy as np

from hex_game0 import BLANK, BLACK, WHITE, BORDER, Hex0


class Hex1(Hex0):
    def __init__(self, game_dim: int):
        self.game_dim = game_dim  # Side length of the game
        self.board_dim = self.game_dim + 2  # Side length of the array repr
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        # Set corners to be borders
        self.board[0] = BORDER
        self.board[self.board_dim-1] = BORDER
        self.board[-self.board_dim] = BORDER
        self.board[-1] = BORDER

        # Set BLACK sides to contain BLACK pieces
        self.board[1:self.board_dim-1] = BLACK  # Left/top
        self.board[self.board_size-self.game_dim-1:-1] = BLACK  # Right/bottom

        # Set WHITE sides to contain WHITE pieces
        for i in range(self.board_dim,
                       self.board_dim*(self.board_dim-1),
                       self.board_dim):  # Left side
            self.board[i] = WHITE
        for i in range((self.board_dim*2)-1,
                       self.board_dim*(self.board_dim-1),
                       self.board_dim):  # Right side
            self.board[i] = WHITE

        self.current_player = BLACK

    def copy(self) -> "Hex1":
        """Return copy"""

        game_copy = Hex1(self.game_dim)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player

        return game_copy


if __name__ == "__main__":
    game = Hex1(8)
    print(game)
