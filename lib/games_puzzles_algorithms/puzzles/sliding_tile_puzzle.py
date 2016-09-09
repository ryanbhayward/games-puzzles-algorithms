import random
from games_puzzles_algorithms.twod_array import TwoDArray


class SlidingTilePuzzle(object):
    """
    A representation of the sliding tile puzzle.
    The puzzle consists of a square board filled with square tiles numbered
    starting from one and one blank space. Tiles adjacent to the blank space
    can slide into it, exchanging the place of the tile and the blank.
    The puzzle is complete when the blank is in the upper left corner and the
    rest of the tiles are in order filling first the top row and then
    successive rows below that from left to right, beginning with tile number 1
    in the space one to the right of the blank and ending with the highest
    numbered tile in the bottom right corner.

    A completed 3 x 3 puzzle:
    _ 1 2
    3 4 5
    6 7 8
    """
    NAME = "sliding_tile"
    BLANK = 0
    DIRECTIONS = {"up": 0, "down": 1, "right": 2, "left": 3}
    HEURISTICS = ["misplaced tiles", "manhattan distance"]

    def __init__(self, size1=3, seed=None, size2=None):
        """
        Initialize a square sliding tile puzzle with size tiles per side.
        The opptional seed argument is used to seed the random number generator
        for randomizing the initial puzzle layerout if it is set,
        so the same puzzle can be generated repeatedly by setting the same seed.
        """

        if seed:
            random.seed(seed)

        self.size1 = size1
        self.size2 = size2
        if size2 is None:
            self.size2 = size1
        self.puzzle = list(range(self.size1 * self.size2))
        random.shuffle(self.puzzle)
        self.puzzle = TwoDArray((self.size1, self.size2), self.puzzle)

        self.num_correct_tiles = 0
        for i in range(self.size1):
            for j in range(self.size2):
                if self.puzzle[(i, j)] == self.BLANK:
                    self.blank_index = (i, j)
                if self.puzzle[(i, j)] == self.correct_num((i, j)):
                    self.num_correct_tiles += 1

    def is_solved(self):
        """Return True if the puzzle is solved. False otherwise."""
        return self.num_correct_tiles == self.size1 * self.size2

    def correct_num(self, position):
        """
        Return the correct number to have at position in the solved puzzle.
        """
        return position[0] * self.size2 + position[1]

    def correct_tile(self, num):
        """Return the correct position for num in the solved puzzle."""
        x = num % self.size2
        y = num // self.size2
        return (y, x)

    def apply_move(self, direction):
        """
        Slide a tile bordering the blank one in direction.
        Raises a Value Error if direction is not in DIRECTIONS or the tile
        the user is attempting to move is off the edge of the puzzle.
        """
        if direction in self.DIRECTIONS:
            direction = self.DIRECTIONS[direction]
        if direction not in self.DIRECTIONS.values():
            raise ValueError("Invalid direction")
        if self.DIRECTIONS["up"] == direction:
            tile = (self.blank_index[0] + 1, self.blank_index[1])
        elif self.DIRECTIONS["down"] == direction:
            tile = (self.blank_index[0] - 1, self.blank_index[1])
        elif self.DIRECTIONS["left"] == direction:
            tile = (self.blank_index[0], self.blank_index[1] + 1)
        elif self.DIRECTIONS["right"] == direction:
            tile = (self.blank_index[0], self.blank_index[1] - 1)
        if (tile[0] >= self.size1 or tile[0] < 0
            or tile[1] >= self.size2 or tile[1] < 0):
            raise ValueError("Invalid move: exceeds puzzle boundaries")

        if self.puzzle[tile] == self.correct_num(tile):
            self.num_correct_tiles -= 1
        elif self.puzzle[tile] == self.correct_num(self.blank_index):
            self.num_correct_tiles += 1
        if self.BLANK == self.correct_num(self.blank_index):
            self.num_correct_tiles -= 1
        elif self.BLANK == self.correct_num(tile):
            self.num_correct_tiles += 1

        self.puzzle[self.blank_index] = self.puzzle[tile]
        self.puzzle[tile] = self.BLANK
        self.blank_index = tile

    def valid_moves(self):
        """Return a list of valid moves."""
        moves = []
        if self.blank_index[0] + 1 < self.size1:
            moves.append(self.DIRECTIONS["up"])
        if self.blank_index[0] - 1 >= 0:
            moves.append(self.DIRECTIONS["down"])
        if self.blank_index[1] + 1 < self.size2:
            moves.append(self.DIRECTIONS["left"])
        if self.blank_index[1] - 1 >= 0:
            moves.append(self.DIRECTIONS["right"])
        return moves

    def str_moves(self, moves):
        strings = []
        for move in moves:
            if move == self.DIRECTIONS["up"]:
                strings.append("up")
            elif move == self.DIRECTIONS["down"]:
                strings.append("down")
            elif move == self.DIRECTIONS["left"]:
                strings.append("left")
            elif move == self.DIRECTIONS["right"]:
                strings.append("right")

        return strings

    def copy(self):
        """Return a deep copy of SlidingTilePuzzle."""
        new_puzzle = SlidingTilePuzzle(1)
        new_puzzle.size1 = self.size1
        new_puzzle.size2 = self.size2
        new_puzzle.num_correct_tiles = self.num_correct_tiles
        new_puzzle.puzzle = TwoDArray((self.size1, self.size2))
        new_puzzle.blank_index = self.blank_index
        for i in range(self.size1):
            for j in range(self.size2):
                new_puzzle.puzzle[(i, j)] = self.puzzle[(i, j)]

        return new_puzzle

    def value(self):
        """Return a tuple representing the puzzle."""
        return tuple(self.puzzle.flatten())

    def equals(self, other):
        """Check if two puzzles are in the same state."""
        return self.puzzle == other.puzzle

    def misplaced_tiles(self):
        """Return a heuristic giving the number of misplaced tiles."""
        return self.size1 * self.size2 - self.num_correct_tiles

    def manhattan_distance(self):
        """
        Return the sum of the distances from the tiles to their goal positions.
        """
        distance = 0
        for i in range(self.size1):
            for j in range(self.size2):
                num = self.puzzle[(i, j)]
                correct = self.correct_tile(num)
                distance += abs(i - correct[0])
                distance += abs(j - correct[1])
        return distance

    def heuristic(self, name):
        """Return a heuristic for the puzzle determined by the string name."""
        if name == "misplaced tiles":
            return self.misplaced_tiles()
        elif name == "manhattan distance":
            return self.manhattan_distance()
        # default to manhattan distane
        return self.manhattan_distance()

    def __str__(self):
        """
        Return a string representation of the puzzle.
        The blank space is represented by an underscore.
        """
        digits = len(str(self.size1 * self.size2 - 1))
        result = ["\n"]
        for i in range(self.size1):
            for j in range(self.size2):
                if (i, j) == self.blank_index:
                    result.append(" " * (digits - 1))
                    result.append("_")
                else:
                    num = str(self.puzzle[(i, j)])
                    result.append(" " * (digits - len(num)))
                    result.append(num)
            result.append("\n")

        space = " "
        return space.join(result)

    def array(self):
        """
        Return an array representation of the puzzle.
        For use in the web visualization. 0 is the blank space.
        :return:
        """
        result = []
        for i in range(self.size1):
            for j in range(self.size2):
                if (i, j) == self.blank_index:
                    result.append(0)
                else:
                    num = self.puzzle.__getitem__([i, j])
                    result.append(int(num))
        return result
