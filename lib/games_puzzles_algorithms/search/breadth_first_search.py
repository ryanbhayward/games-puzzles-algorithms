from collections import deque
import time
from games_puzzles_algorithms.search.search import Search, Node


class BreadthFirstSearch(Search):
    """Breadth first search class."""

    def __init__(self, problem, time_limit):
        """
        Initialize the search.
        Create the root node with the problem and set a time limit for search.
        """
        Search.__init__(self, problem, time_limit)
        self.frontier = deque()
        self.frontier.append(self.rootnode)

    def search(self, verbose=False):
        """
        Perform breadth first search until time_limit is reached.
        Returns a list of moves to reach the solution if it finds one, None
        if there is not solution, or False if the time limit is reached.
        """
        start = time.time()
        if self.rootnode.state.is_solved():
            return self._solution(self.rootnode)

        tick = 0

        while time.time() - start < self.time_limit:
            solved, state = self.step(verbose, tick)
            if solved is None:
                return None
            if solved:
                return state
            tick += 1
        return False

    def _in_frontier(self, state):
        """Check if there is a node with state state in the frontier."""
        for node in self.frontier:
            if state.equals(node.state):
                return True

        return False

    def step(self, verbose=False, tick=0):
        """
        Perform one step of the search.
        :param verbose: boolean, verbose mode
        :param tick: integer, number of steps elapsed
        :return: 2-tuple.
        * (None, None) for no solution,
        * (True, [Steps]) for solved,
        * (False, <state>) for unsolved, searching
        """
        if len(self.frontier) == 0:
            return None, None

        current_node = self.frontier.popleft()

        if current_node.state.is_solved():
            return True, []

        if verbose:
            print("Step {0}".format(tick))
            print(current_node.state)

        self.explored.add(current_node.state.value())
        for move in current_node.state.valid_moves():
            new_state = current_node.state.copy()
            new_state.apply_move(move)
            child = Node(new_state, move, current_node)
            if not new_state.value() in self.explored and not self._in_frontier(new_state):
                if child.state.is_solved():
                    if verbose:
                        print("Took {0} steps using Breadth First Search.".format(tick))
                    return True, self.solution(child)
                self.frontier.append(child)

        return False, current_node.state

    def reset(self):
        self.frontier = deque()
        self.frontier.append(self.rootnode)
        self.explored = set()
        self.solved = False
