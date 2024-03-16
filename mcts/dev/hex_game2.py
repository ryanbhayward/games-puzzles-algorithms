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
# Where BOARDER = 3, BLACK = 1, WHITE = 2, BLANK = 0


from copy import deepcopy
import numpy as np

from hex_game0 import Hex0, BLANK, BLACK, WHITE, BORDER
from union_find import UnionFind


class Hex2(Hex0):
    def __init__(self, game_dim: int, is_copy: bool = False):
        self.game_dim = game_dim
        self.board_dim = self.game_dim + 2
        self.board_size = self.board_dim ** 2
        self.board = np.array([BLANK] * self.board_size)

        self.current_player = BLACK
        self.union_find = None

        if not is_copy:
            self.union_find = UnionFind(self.board_size)
            self.board[0] = BORDER
            self.board[self.board_dim-1] = BORDER
            self.board[-self.board_dim] = BORDER
            self.board[-1] = BORDER

            # Initialize top row
            for i in range(1, self.board_dim-1):
                self.board[i] = BLACK
                if i > 1:
                    self.union_find.union(i-1, i)

            # Initialize bottom row
            for i in range(self.board_size-self.game_dim-1, self.board_size-1):
                self.board[i] = BLACK
                if i > self.board_size-self.game_dim-1:
                    self.union_find.union(i-1, i)

            # Initialize left side
            for i in range(self.board_dim,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > self.board_dim:
                    self.union_find.union(i-self.board_dim, i)

            # Initialize right side
            for i in range((self.board_dim*2)-1,
                           (self.board_dim-1)*self.board_dim,
                           self.board_dim):
                self.board[i] = WHITE
                if i > (self.board_dim*2)-1:
                    self.union_find.union(i-self.board_dim, i)

    def play_move(self, move: int, player: int = None) -> bool:
        """
        Play a move, update the current player, check for win.

        Parameters:
        move (int): Position of move
        player (int): WHITE or BLACK, player to move
        """

        if type(move) is list:
            move = self._2d_to_1d(move)

        if player is None:
            player = self.current_player

        self.board[move] = player
        self.current_player = 3 - self.current_player  # Switch player

        neighbours = self._get_neighbours(move)
        for neighbour_move in neighbours:
            if self.board[neighbour_move] == player:
                self.union_find.union(neighbour_move, move)

    def check_win(self, *args) -> bool:
        """
        Check if the game has been won.

        Uses Union Find data structure to check if two sides of the
        same color are in the same set (i.e. touching).

        Since this function is called only in the play_move function,
        we only need to consider if the game has been won, not who
        has won it. The player who made the last move is known by
        play_move, and will be the winner if the game has been won.

        Returns:
        bool: True if the game has been won
        """

        if self.union_find.find(1) == self.union_find.find(self.board_size-2):
            return True

        if (self.union_find.find(self.board_dim)
                == self.union_find.find((self.board_dim*2)-1)):
            return True

        return False

    def copy(self) -> "Hex2":
        """Return copy"""

        game_copy = Hex2(self.game_dim, is_copy=True)
        game_copy.board = deepcopy(self.board)
        game_copy.current_player = self.current_player
        game_copy.union_find = deepcopy(self.union_find)

        return game_copy
