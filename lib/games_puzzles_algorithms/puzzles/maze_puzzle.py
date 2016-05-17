#!/usr/bin/env python3

import copy
import random
from math import hypot


class MazePuzzle(object):
    """
    Representation of a maze object. Grid, 2 dimensional.
    Goal is to navigate from [0,0] to [width-1, height-1]

    e.g. (5 by 5):
           +---+---+---+---+---+
      Y 4  |                 $ |
           +---+---+   +---+   +
      Y 3  |       |   |       |
           +   +   +   +   +---+
      Y 2  |   |   |   |       |
           +   +   +---+---+   +
      Y 1  |   |               |
           +   +---+---+---+   +
      Y 0  | @         |       |
           +---+---+---+---+---+
            X0  X1  X2  X3  X4

        Shortest Path from (0, 0) to (4, 4) is
          [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3), (1, 2), (1, 1), (2, 1), (3, 1), (4, 1), (4, 2), (3, 2), (3, 3),
            (4, 3), (4, 4)]
        Directions list from (0, 0) to (4, 4) is
          ['up', 'up', 'up', 'right', 'down', 'down', 'right', 'right', 'right', 'up', 'left', 'up', 'right', 'up']
    """

    # Static variables
    NAME = "maze"
    PLAYER = " @ "
    FINISH = " $ "
    DIRECTIONS = {
        "up": "up",
        "down": "down",
        "left": "left",
        "right": "right"
    }
    MOVE_DIRECTIONS = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0)
    }

    def __init__(self, width=5, height=5, seed=None):
        """
        Construct the maze based on the given width and height.
        All constructed mazes guarantee no loops and end to end visibility.

        :param width: Size of the maze by x axis
        :param height: Size of the maze by y axis
        """

        self.ver = [["|   "] * width + ['|'] for _ in range(height)] + [[]]
        self.hor = [["+---"] * width + ['+'] for _ in range(height + 1)]
        self.position = [0, 0]
        self.goal = [width - 1, height - 1]

        vis = [[0] * width + [1] for _ in range(height)] + [[1] * (width + 1)]
        if seed:
            random.seed(seed)

        def construct_walk(x=0, y=0):
            vis[y][x] = 1
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]

            random.shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]:
                    continue
                if xx == x:
                    self.hor[max(y, yy)][x] = "+   "
                if yy == y:
                    self.ver[y][max(x, xx)] = "    "
                construct_walk(xx, yy)

        construct_walk()

    def __str__(self):
        """
        Return the string representation of the maze with the player and finish line.
        :return:
        """
        ver_with_players = copy.deepcopy(self.ver)
        vis_yx = [(len(self.ver) - 2) - self.goal[1], self.goal[0]]
        if ver_with_players[vis_yx[0]][vis_yx[1]] == "|   ":
            ver_with_players[vis_yx[0]][vis_yx[1]] = "|" + MazePuzzle.FINISH
        else:
            ver_with_players[vis_yx[0]][vis_yx[1]] = " " + MazePuzzle.FINISH
        vis_yx = [(len(self.ver) - 2) - self.position[1], self.position[0]]
        if ver_with_players[vis_yx[0]][vis_yx[1]] == "|   ":
            ver_with_players[vis_yx[0]][vis_yx[1]] = "|" + MazePuzzle.PLAYER
        else:
            ver_with_players[vis_yx[0]][vis_yx[1]] = " " + MazePuzzle.PLAYER

        s = ""
        for (a, b) in zip(self.hor, ver_with_players):
            s += ''.join(a + ['\n'] + b + ['\n'])
        return s

    def __eq__(self, other):
        """
        Check if self is equal to other.
        :param other: Another object
        :return: True if equality passes, false otherwise
        """
        type_match = isinstance(other, self.__class__)
        if not type_match:
            return False
        return self.position == other.position and self.goal == other.goal and \
            self.hor == other.hor and self.ver == other.ver

    def is_solved(self):
        """
        Return if the maze is solved yet.
        :return: True if solved, False otherwise
        """
        return self.position == self.goal

    def valid_moves(self):
        """
        Return a list of valid moves.
        :return: Array of moves.
        """
        valid_moves = []
        # Can move left
        if "|" not in self.ver[len(self.ver) - 2 - self.position[1]][self.position[0]]:
            valid_moves.append(MazePuzzle.DIRECTIONS["left"])
        # Can move right
        if "|" not in self.ver[len(self.ver) - 2 - self.position[1]][self.position[0] + 1]:
            valid_moves.append(MazePuzzle.DIRECTIONS["right"])
        # Can move up
        if "-" not in self.hor[len(self.hor) - 2 - self.position[1]][self.position[0]]:
            valid_moves.append(MazePuzzle.DIRECTIONS["up"])
        # Can move down
        if "-" not in self.hor[len(self.hor) - 1 - self.position[1]][self.position[0]]:
            valid_moves.append(MazePuzzle.DIRECTIONS["down"])
        return valid_moves

    @staticmethod
    def str_moves(moves):
        """
        Given a list of moves, return the string list of moves
        :param moves: list of move objects (dict with move tuple)
        :return: list of strings representing the moves
        """
        move_strings = []
        for move in moves:
            if move == MazePuzzle.DIRECTIONS["up"]:
                move_strings.append("up")
            elif move == MazePuzzle.DIRECTIONS["down"]:
                move_strings.append("down")
            elif move == MazePuzzle.DIRECTIONS["left"]:
                move_strings.append("left")
            elif move == MazePuzzle.DIRECTIONS["right"]:
                move_strings.append("right")
        return move_strings

    def apply_move(self, direction):
        """
        Move the player within the maze. If the movement is invalid, print a message, do nothing.
        :param direction: String, direction to move in
        :return: None
        """
        str_direction = str(direction).lower()
        if str_direction not in MazePuzzle.DIRECTIONS:
            print("Invalid direction: " + str_direction)
            return
        if str_direction not in MazePuzzle.str_moves(self.valid_moves()):
            print("Path blocked in: " + str_direction)
            return
        move_player = MazePuzzle.MOVE_DIRECTIONS[str_direction]
        self.position = [x + y for x, y in zip(self.position, move_player)]

    def __raw_dist_to_finish(self):
        """
        Return the raw pythagorean distance from the player position to the goal.
        :return:
        """
        return hypot(self.goal[0] - self.position[0], self.goal[1] - self.position[1])

    # noinspection PyUnusedLocal
    def heuristic(self, name):
        """
        Calculate heuristic for maze completion
        :param name: ignoring the heuristic, only one heuristic (pythagorean dist).
         Placed for compatibility with existing search methods
        :return:
        """
        return self.__raw_dist_to_finish()

    def value(self):
        """
        Return the string version of self.
        :return:
        """
        return str(self)

    def copy(self):
        """
        Return a new object representing self.
        :return:
        """
        new_maze = MazePuzzle()
        new_maze.ver = copy.deepcopy(self.ver)
        new_maze.hor = copy.deepcopy(self.hor)
        new_maze.position = self.position[:]
        new_maze.goal = self.goal[:]
        return new_maze

    def equals(self, other):
        """Check if two puzzles are in the same state."""
        return self == other
