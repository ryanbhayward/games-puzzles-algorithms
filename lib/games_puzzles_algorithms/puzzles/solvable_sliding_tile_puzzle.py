from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.twod_array import TwoDArray
import random


class SolvableSlidingTilePuzzle(SlidingTilePuzzle):
    """A representation of a sliding tile puzzle guaranteed to be solvable."""
    
    def __init__(self, size1=3, seed=None, size2=None):
        """
        Initialize a rectangular sliding tile puzzle with size1 * size2 tiles.
        size1 gives the number of rows. The number of columns is given by size2
        or size1 if size2 is None.
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
        self.puzzle = TwoDArray((self.size1, self.size2), self.puzzle)
        
        self.num_correct_tiles = 0
        for i in range(self.size1):
            for j in range(self.size2):
                if self.puzzle[(i, j)] == self.BLANK:
                    self.blank_index = (i, j)
                if self.puzzle[(i, j)] == self.correct_num((i, j)):
                    self.num_correct_tiles += 1
        
        for i in range(self.size1 * self.size2 * 10):
            moves = self.valid_moves()
            self.apply_move(random.choice(moves))