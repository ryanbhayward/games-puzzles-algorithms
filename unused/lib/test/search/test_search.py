from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.search.search import Search, Node
import unittest

def dummy_return1(unused):
    return 1

def dummy_return2(unused):
    return 2

class TestNode(unittest.TestCase):
    
    def setUp(self):
        self.state = SlidingTilePuzzle(3)
        self.heuristic = "misplaced tiles"
        self.move = SlidingTilePuzzle.DIRECTIONS['up']
        self.node = Node(self.state, self.move, None, self.heuristic)        

    def test_init(self):
        self.assertTrue(self.state.equals(self.node.state))
        self.assertEqual(self.node.heuristic_name, self.heuristic)
        self.assertEqual(self.node.move, self.move)
        self.assertEqual(self.node.parent, None)
        self.assertEqual(self.node.level, 0)
        
    def test_set_heuristic(self):
        new_heuristic = 'manhattan distance'
        self.node.set_heuristic(new_heuristic)
        self.assertEqual(self.node.heuristic_name, new_heuristic)
        
    def test_eq_true(self):
        other_state = SlidingTilePuzzle(3)
        other_node = Node(other_state, self.move, None, self.heuristic)
        self.state.heuristic = dummy_return1
        other_state.heuristic = dummy_return1
        self.assertEqual(self.node, other_node)
        
    def test_eq_false(self):
        other_state = SlidingTilePuzzle(3)
        other_node = Node(other_state, self.move, self.node, self.heuristic)
        self.state.heuristic = dummy_return1
        other_state.heuristic = dummy_return1
        self.assertNotEqual(self.node, other_node)
        
    def test_lt_true(self):
        other_state = SlidingTilePuzzle(3)
        other_node = Node(other_state, self.move, None, self.heuristic)
        self.state.heuristic = dummy_return1
        other_state.heuristic = dummy_return2
        self.assertTrue(self.node < other_node)
        
    def test_lt_false(self):
        other_state = SlidingTilePuzzle(3)
        other_node = Node(other_state, self.move, None, self.heuristic)
        self.state.heuristic = dummy_return2
        other_state.heuristic = dummy_return1
        self.assertFalse(self.node < other_node)        


class TestSearch(unittest.TestCase):
    
    def setUp(self):
        self.state = SlidingTilePuzzle(3)
        self.time = 10
        self.search = Search(self.state, self.time)
    
    def test_init(self):
        self.assertEqual(self.search.time_limit, self.time)
        self.assertEqual(len(self.search.explored), 0)
        self.assertEqual(self.search.rootnode.state, self.state)
        
    def test_search(self):
        with self.assertRaises(NotImplementedError):
            self.search.search()
            
    def test_solution(self):
        time = 10
        root_state = SlidingTilePuzzle(3, 1)
        heuristic = "misplaced tiles"
        move1 = SlidingTilePuzzle.DIRECTIONS['up']
        move2 = SlidingTilePuzzle.DIRECTIONS['right']
        move3 = SlidingTilePuzzle.DIRECTIONS['down']
        state1 = root_state.copy()
        state1.apply_move(move1)
        state2 = state1.copy()
        state2.apply_move(move2)
        state3 = state2.copy()
        state3.apply_move(move3)
        search = Search(root_state, time)
        node1 = Node(state1, move1, search.rootnode, heuristic)
        node2 = Node(state2, move2, node1, heuristic)
        node3 = Node(state3, move3, node2, heuristic)
        self.assertEqual(search.solution(node3), [move1, move2, move3])


if __name__ == '__main__':
    unittest.main()