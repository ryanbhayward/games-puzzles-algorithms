from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.search.search import Node
from games_puzzles_algorithms.search.a_star import AStar
import unittest

class TestAStar(unittest.TestCase):
    
    def test_init(self):
        state = SlidingTilePuzzle(3)
        time = 10
        heuristic = 'misplaced tiles'
        search = AStar(state, time, heuristic)
        self.assertEqual(search.time_limit, time)
        self.assertEqual(len(search.explored), 0)
        self.assertEqual(search.rootnode.state, state)
        self.assertEqual(search.heuristic, heuristic)
        self.assertEqual(search.rootnode.heuristic_name, heuristic)
        self.assertEqual(len(search.frontier), 1)

    def test_update_frontier_false(self):
        state = SlidingTilePuzzle(3, 1)
        time = 10
        heuristic = 'misplaced tiles'
        search = AStar(state, time, heuristic)
        state2 = SlidingTilePuzzle(3, 2)
        move = SlidingTilePuzzle.DIRECTIONS['up']
        node = Node(state2, move, search.rootnode, heuristic)
        self.assertFalse(search._update_frontier(node))

    def test_update_frontier_true(self):
        state = SlidingTilePuzzle(3, 1)
        time = 10
        heuristic = 'misplaced tiles'
        search = AStar(state, time, heuristic)
        search.rootnode.level = 2
        state2 = SlidingTilePuzzle(3, 1)
        move = SlidingTilePuzzle.DIRECTIONS['up']
        node = Node(state2, move, None, heuristic)
        self.assertTrue(search._update_frontier(node))
        self.assertIn(node, search.frontier)
        self.assertNotIn(search.rootnode, search.frontier)

    def test_search_no_solution(self):
        state = SlidingTilePuzzle(2, 1)
        time = 5
        heuristic = 'misplaced tiles'
        search = AStar(state, time, heuristic)
        self.assertEqual(search.search(), None)        

    def test_search_misplaced_tiles(self):
        state = SlidingTilePuzzle(2, 10)
        time = 5
        heuristic = 'misplaced tiles'
        search = AStar(state, time, heuristic)
        solution = search.search()
        for move in solution:
            state.apply_move(move)
            
        self.assertTrue(state.is_solved())        

    def test_search_manhattan_distance(self):
        state = SlidingTilePuzzle(2, 10)
        time = 5
        heuristic = 'manhattan distance'
        search = AStar(state, time, heuristic)
        solution = search.search()
        for move in solution:
            state.apply_move(move)
            
        self.assertTrue(state.is_solved())


if __name__ == '__main__':
    unittest.main()