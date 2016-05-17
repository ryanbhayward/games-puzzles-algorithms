from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.search.breadth_first_search import BreadthFirstSearch
import unittest

class TestBreadthFirstSearch(unittest.TestCase):
    
    def test_init(self):
        state = SlidingTilePuzzle(3)
        time = 10
        search = BreadthFirstSearch(state, time)
        self.assertEqual(search.time_limit, time)
        self.assertEqual(len(search.explored), 0)
        self.assertEqual(search.rootnode.state, state)
        self.assertEqual(len(search.frontier), 1)
        
    def test_in_frontier_true(self):
        state1 = SlidingTilePuzzle(3, 1)
        state2 = SlidingTilePuzzle(3, 1)
        time = 10
        search = BreadthFirstSearch(state1, time)
        self.assertTrue(search._in_frontier(state2))
        
    def test_in_frontier_false(self):
        state1 = SlidingTilePuzzle(3, 1)
        state2 = SlidingTilePuzzle(3, 2)
        time = 10
        search = BreadthFirstSearch(state1, time)
        self.assertFalse(search._in_frontier(state2))
        
    def test_num_nodes_generated(self):
        state = SlidingTilePuzzle(3)
        time = 10
        search = BreadthFirstSearch(state, time)
        self.assertEqual(search.num_nodes_generated(), 1)
        
    def test_search_no_solution(self):
        state = SlidingTilePuzzle(2, 1)
        time = 5
        search = BreadthFirstSearch(state, time)
        self.assertEqual(search.search(), None)
        
    def test_search_solution(self):
        state = SlidingTilePuzzle(2, 10)
        time = 5
        search = BreadthFirstSearch(state, time)
        solution = search.search()
        for move in solution:
            state.apply_move(move)
            
        self.assertTrue(state.is_solved())


if __name__ == '__main__':
    unittest.main()