from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.puzzles.solvable_sliding_tile_puzzle import SolvableSlidingTilePuzzle
import unittest
import random

class TestSlidingTilePuzzle(unittest.TestCase):
    
    def test_init(self):
        size = 3
        puzzle = SlidingTilePuzzle(size)
        self.assertEqual(puzzle.size1, size)
        self.assertEqual(puzzle.size2, size)
        self.assertEqual(puzzle.puzzle.shape, (size, size))
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)
        self.assertLessEqual(puzzle.num_correct_tiles, size * size)
        self.assertGreaterEqual(puzzle.num_correct_tiles, 0)

    def test_seed_init(self):
        size = 3
        seed = 1
        a = SlidingTilePuzzle(size, seed)
        b = SlidingTilePuzzle(size, seed)
        self.assertEqual(a.size1, b.size1)
        self.assertEqual(a.size2, b.size2)
        for i in range(size):
            for j in range(size):
                self.assertEqual(a.puzzle[(i, j)], b.puzzle[(i, j)])
        self.assertEqual(a.blank_index, b.blank_index)
        self.assertEqual(a.num_correct_tiles, b.num_correct_tiles)
        
    def test_init_rectangle(self):
        size1 = 2
        size2 = 3
        puzzle = SlidingTilePuzzle(size1=size1, size2=size2)
        self.assertEqual(puzzle.size1, size1)
        self.assertEqual(puzzle.size2, size2)
        self.assertEqual(puzzle.puzzle.shape, (size1, size2))
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)
        self.assertLessEqual(puzzle.num_correct_tiles, size1 * size2)
        self.assertGreaterEqual(puzzle.num_correct_tiles, 0)        

    def test_is_solved_false(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        self.assertFalse(puzzle.is_solved())

    def test_is_solved_true(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["up"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["left"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        self.assertTrue(puzzle.is_solved())

    def test_correct_num(self):
        size = 3
        puzzle = SlidingTilePuzzle(size)
        number = 0
        for i in range(size):
            for j in range(size):
                self.assertEqual(puzzle.correct_num((i, j)), number)
                number += 1
                
    def test_correct_num_rectangle(self):
        size1 = 3
        size2 = 2
        puzzle = SlidingTilePuzzle(size1=size1, size2=size2)
        number = 0
        for i in range(size1):
            for j in range(size2):
                self.assertEqual(puzzle.correct_num((i, j)), number)
                number += 1

    def test_correct_tile(self):
        size = 3
        puzzle = SlidingTilePuzzle(size)
        number = 0
        for i in range(size):
            for j in range(size):
                self.assertEqual(puzzle.correct_tile(number), (i, j))
                number += 1
                
    def test_correct_tile_rectangle(self):
        size1 = 2
        size2 = 3
        puzzle = SlidingTilePuzzle(size1=size1, size2=size2)
        number = 0
        for i in range(size1):
            for j in range(size2):
                self.assertEqual(puzzle.correct_tile(number), (i, j))
                number += 1

    def test_apply_move_up(self):
        size = 2
        seed = 5
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS['up'])
        self.assertEqual(puzzle.puzzle[(0, 0)], 3)
        self.assertEqual(puzzle.puzzle[(0, 1)], 1)
        self.assertEqual(puzzle.puzzle[(1, 0)], 0)
        self.assertEqual(puzzle.puzzle[(1, 1)], 2)
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)        

    def test_apply_move_down(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS['down'])
        self.assertEqual(puzzle.puzzle[(0, 0)], 3)
        self.assertEqual(puzzle.puzzle[(0, 1)], 0)
        self.assertEqual(puzzle.puzzle[(1, 0)], 1)
        self.assertEqual(puzzle.puzzle[(1, 1)], 2)
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)

    def test_apply_move_left(self):
        size = 2
        seed = 5
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS['left'])
        self.assertEqual(puzzle.puzzle[(0, 0)], 1)
        self.assertEqual(puzzle.puzzle[(0, 1)], 0)
        self.assertEqual(puzzle.puzzle[(1, 0)], 3)
        self.assertEqual(puzzle.puzzle[(1, 1)], 2)
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)        

    def test_apply_move_right(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS['right'])
        self.assertEqual(puzzle.puzzle[(0, 0)], 3)
        self.assertEqual(puzzle.puzzle[(0, 1)], 2)
        self.assertEqual(puzzle.puzzle[(1, 0)], 0)
        self.assertEqual(puzzle.puzzle[(1, 1)], 1)
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)

    def test_valid_moves_some(self):
        size = 2
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        moves = puzzle.valid_moves()
        moves.sort()
        expected_moves = [SlidingTilePuzzle.DIRECTIONS['up'],
                          SlidingTilePuzzle.DIRECTIONS['right']]
        expected_moves.sort()
        self.assertEqual(moves, expected_moves)

    def test_valid_moves_all(self):
        size = 4
        seed = 2
        puzzle = SlidingTilePuzzle(size, seed)
        moves = puzzle.valid_moves()
        moves.sort()
        expected_moves = [SlidingTilePuzzle.DIRECTIONS['up'],
                          SlidingTilePuzzle.DIRECTIONS['left'],
                          SlidingTilePuzzle.DIRECTIONS['down'],
                          SlidingTilePuzzle.DIRECTIONS['right']]
        expected_moves.sort()
        self.assertEqual(moves, expected_moves)

    def test_str_moves(self):
        size = 4
        seed = 2
        puzzle = SlidingTilePuzzle(size, seed)
        moves = puzzle.valid_moves()        
        string_moves = puzzle.str_moves(moves)
        string_moves.sort()
        expected_moves = ['up', 'down', 'left', 'right']
        expected_moves.sort()
        self.assertEqual(string_moves, expected_moves)

    def test_copy(self):
        size = 3
        a = SlidingTilePuzzle(size)
        b = a.copy()
        self.assertEqual(a.size1, b.size1)
        self.assertEqual(a.size2, b.size2)
        for i in range(size):
            for j in range(size):
                self.assertEqual(a.puzzle[(i, j)], b.puzzle[(i, j)])
        self.assertEqual(a.blank_index, b.blank_index)
        self.assertEqual(a.num_correct_tiles, b.num_correct_tiles)

    def test_value(self):
        size = 2
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle_value = puzzle.value()
        expected_value = (3, 0, 2, 1)
        self.assertEqual(puzzle_value, expected_value)

    def test_equals_true(self):
        size = 3
        seed = 1
        a = SlidingTilePuzzle(size, seed)
        b = SlidingTilePuzzle(size, seed)
        self.assertTrue(a.equals(b))

    def test_equals_false(self):
        size = 3
        seed1 = 1
        seed2 = 2
        a = SlidingTilePuzzle(size, seed1)
        b = SlidingTilePuzzle(size, seed2)
        self.assertFalse(a.equals(b))

    def test_misplaced_tiles_some(self):
        size = 3
        seed = 4
        puzzle = SlidingTilePuzzle(size, seed)
        num_tiles = puzzle.misplaced_tiles()
        expected_num = 8
        self.assertEqual(num_tiles, expected_num)

    def test_misplaced_tiles_none(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["up"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["left"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        num_tiles = puzzle.misplaced_tiles()
        expected_num = 0
        self.assertEqual(num_tiles, expected_num)
        
    def test_misplaced_tiles_rectangle(self):
        size1 = 2
        size2 = 3
        seed = 1
        puzzle = SlidingTilePuzzle(size1, seed, size2)
        num_tiles = puzzle.misplaced_tiles()
        expected_num = 5
        self.assertEqual(num_tiles, expected_num)

    def test_manhattan_distance_incomplete(self):
        size = 3
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        distance = puzzle.manhattan_distance()
        expected_distance = 3 + 2 + 2 + 1 + 1 + 3 + 3 + 3 + 2
        self.assertEqual(distance, expected_distance)

    def test_manhattan_distance_complete(self):
        size = 2
        seed = 10
        puzzle = SlidingTilePuzzle(size, seed)
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["up"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["left"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["down"])
        puzzle.apply_move(SlidingTilePuzzle.DIRECTIONS["right"])
        num_tiles = puzzle.manhattan_distance()
        expected_num = 0
        self.assertEqual(num_tiles, expected_num)
        
    def test_manhattan_distance_rectangle(self):
        size1 = 2
        size2 = 3
        seed = 1
        puzzle = SlidingTilePuzzle(size1, seed, size2)
        num_tiles = puzzle.manhattan_distance()
        expected_num = 1 + 2 + 2 + 2 + 0 + 1
        self.assertEqual(num_tiles, expected_num)

    def test_heuristic_misplaced(self):
        size = 3
        seed = 4
        puzzle = SlidingTilePuzzle(size, seed)
        num_tiles = puzzle.heuristic('misplaced tiles')
        expected_num = 8
        self.assertEqual(num_tiles, expected_num)

    def test_heuristic_manhattan(self):
        size = 3
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        distance = puzzle.heuristic('manhattan distance')
        expected_distance = 3 + 2 + 2 + 1 + 1 + 3 + 3 + 3 + 2
        self.assertEqual(distance, expected_distance) 

    def test_str_single_digits(self):
        size = 2
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        expected_str = '\n  3  B \n  2  1 \n'
        self.assertEqual(str(puzzle), expected_str)

    def test_str_double_digits(self):
        size = 4
        seed = 1
        puzzle = SlidingTilePuzzle(size, seed)
        expected_str = ('\n   2  10   B  14 '
                        '\n   6   5   3   8 '
                        '\n   7  11  15   1 '
                        '\n  12  13   9   4 \n')
        self.assertEqual(str(puzzle), expected_str)
        
    def test_str_rectangle(self):
        size1 = 2
        size2 = 3
        seed = 1
        puzzle = SlidingTilePuzzle(size1, seed, size2)
        expected_str = '\n  2  3  5 \n  B  4  1 \n'
        self.assertEqual(str(puzzle), expected_str)
        

def reverse_move(move):
    if move == SlidingTilePuzzle.DIRECTIONS['up']:
        return SlidingTilePuzzle.DIRECTIONS['down']
    elif move == SlidingTilePuzzle.DIRECTIONS['down']:
        return SlidingTilePuzzle.DIRECTIONS['up']
    elif move == SlidingTilePuzzle.DIRECTIONS['left']:
        return SlidingTilePuzzle.DIRECTIONS['right']
    else:
        return SlidingTilePuzzle.DIRECTIONS['left']


class TestSolvableSlidingTilePuzzle(unittest.TestCase):
    
    def test_init(self):
        size = 3
        puzzle = SolvableSlidingTilePuzzle(size)
        self.assertEqual(puzzle.size1, size)
        self.assertEqual(puzzle.size2, size)
        self.assertEqual(puzzle.puzzle.shape, (size, size))
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)
        self.assertLessEqual(puzzle.num_correct_tiles, size * size)
        self.assertGreaterEqual(puzzle.num_correct_tiles, 0)

    def test_seed_init(self):
        size = 3
        seed = 1
        a = SolvableSlidingTilePuzzle(size, seed)
        b = SolvableSlidingTilePuzzle(size, seed)
        self.assertEqual(a.size1, b.size1)
        self.assertEqual(a.size2, b.size2)
        for i in range(size):
            for j in range(size):
                self.assertEqual(a.puzzle[(i, j)], b.puzzle[(i, j)])
        self.assertEqual(a.blank_index, b.blank_index)
        self.assertEqual(a.num_correct_tiles, b.num_correct_tiles)
        random.seed(seed)
        moves = []
        number = 0
        
        for i in range(size):
            for j in range(size):
                b.puzzle[(i, j)] = number
                number += 1
        b.blank_index = (0, 0)
        
        for i in range(size * size * 10):
            move_choice = b.valid_moves()
            move = random.choice(move_choice)
            b.apply_move(move)
            moves.append(reverse_move(move))

        moves.reverse()
        for move in moves:
            a.apply_move(move)
        self.assertTrue(a.is_solved())
        
        
    def test_init_rectangle(self):
        size1 = 2
        size2 = 3
        puzzle = SolvableSlidingTilePuzzle(size1=size1, size2=size2)
        self.assertEqual(puzzle.size1, size1)
        self.assertEqual(puzzle.size2, size2)
        self.assertEqual(puzzle.puzzle.shape, (size1, size2))
        self.assertEqual(puzzle.puzzle[puzzle.blank_index], 0)
        self.assertLessEqual(puzzle.num_correct_tiles, size1 * size2)
        self.assertGreaterEqual(puzzle.num_correct_tiles, 0)   


if __name__ == '__main__':
    unittest.main()
