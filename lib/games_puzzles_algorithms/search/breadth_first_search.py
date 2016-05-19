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
        start_time = time.time()
        if self.verbose:
            print('Starting Breadth First Search')
            self.print_verbose_statement(start_time)
            verbose_limit = 10


        if self.rootnode.state.is_solved():
            if self.verbose:
                print('The rootnode was a solution node.')
                self.print_verbose_statement(start_time)
            return self.solution(self.rootnode)
        while time.time() - start_time < self.time_limit:
            if self.verbose and time.time() - start_time > verbose_limit:
                self.print_verbose_statement(start_time)
                verbose_limit += 10
            if len(self.frontier) == 0:
                if self.verbose:
                    print('0 nodes are left in the frontier,'
                          ' and the puzzle has no solution.')
                    self.print_verbose_statement(start_time)
                    print('Ending the search.')
                return None
            current_node = self.frontier.popleft()

            if verbose:
                print("Step {0}".format(tick))
                print(current_node.state)

            self.explored.add(current_node.state.value())
            for move in current_node.state.valid_moves():
                new_state = current_node.state.copy()
                new_state.apply_move(move)
                child = Node(new_state, move, current_node)
                if (not new_state.value() in self.explored
                    and not self._in_frontier(new_state)):
                    if child.state.is_solved():
                        if self.verbose:
                            print('Solution node found')
                            self.print_verbose_statement(start_time)
                        return self.solution(child)
                    self.frontier.append(child)

        if self.verbose:
            self.print_verbose_statement(start_time)
            print('The search timed out without finding a solution.')
        return False

    def _in_frontier(self, state):
        """Check if there is a node with state state in the frontier."""
        for node in self.frontier:
            if state.equals(node.state):
                return True

        return False
