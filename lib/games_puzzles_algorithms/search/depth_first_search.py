import time
from games_puzzles_algorithms.search.search import Search, Node


class DepthFirstSearch(Search):
    """Depth first search class."""

    def __init__(self, problem, time_limit):
        """
        Initialize the search.
        Create the root node with the problem and set a time limit for search.
        """
        Search.__init__(self, problem, time_limit)
        self.frontier = []
        self.frontier.append(self.rootnode)

    def search(self, verbose=False):
        """
        Perform depth first search until time_limit is reached.
        Returns a list of moves to reach the solution if it finds one, None
        if there is not solution, or False if the time limit is reached.
        """
        start = time.time()
        if self.rootnode.state.is_solved():
            return self._solution(self.rootnode)

        tick = 0

        while time.time() - start < self.time_limit:
            if len(self.frontier) == 0:
                return None
            current_node = self.frontier.pop()

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
                            print("Took {0} steps using Depth First Search.".format(tick))
                        return self.solution(child)
                    self.frontier.append(child)
            tick += 1
        return False

    def _in_frontier(self, state):
        """Check if there is a node with state state in the frontier."""
        for node in self.frontier:
            if state.equals(node.state):
                return True

        return False
