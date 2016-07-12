from games_puzzles_algorithms.search.search import Search, Node
from heapq import *
import time


class AStar(Search):
    """
    A* search class.
    """

    def __init__(self, problem, time_limit, heuristic):
        """
        Initialize the search.
        Create the root node with the problem and set a time limit for search.
        Heursitic is a string indicating the name of the heuristic to use.
        """
        Search.__init__(self, problem, time_limit)
        self.frontier = []
        self.rootnode.set_heuristic(heuristic)
        self.heuristic = heuristic
        heappush(self.frontier, self.rootnode)

    def search(self, verbose=False):
        """
        Perform A* until time_limit is reached.
        Returns a list of moves to reach the solution if it finds one, None
        if there is not solution, or False if the time limit is reached.
        """
        if self.solved:
            self.reset()
        start_time = time.time()
        tick = 0
        while time.time() - start_time < self.time_limit:
            solved, state = self.step(verbose, tick)
            self.solved = solved
            if solved is None:
                return None
            if solved:
                return state
            tick += 1
        return False

    def _update_frontier(self, node):
        """Update the frontier except for adding new nodes.
        Return True if there is a node (A) in the frontier with the same
        state as node node, False otherwise. If A has a higher cost than node
        replace A with node in the frontier and reorder the frontier.
        """
        for i in range(len(self.frontier)):
            if self.frontier[i].state.equals(node.state):
                if self.frontier[i] > node:
                    self.frontier[i] = node
                    heapify(self.frontier)
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
        current_node = heappop(self.frontier)

        if verbose:
            print("Step {0}".format(tick))
            print(current_node.state)

        if current_node.state.is_solved():
            if verbose:
                print("Took {0} steps using A Star.".format(tick))
            return True, self.solution(current_node)

        self.explored.add(current_node.state.value())
        for move in current_node.state.valid_moves():
            new_state = current_node.state.copy()
            new_state.apply_move(move)
            child = Node(new_state, move, current_node, self.heuristic)
            in_frontier = self._update_frontier(child)
            if not (new_state.value() in self.explored or in_frontier):
                heappush(self.frontier, child)

        return False, current_node.state

    def reset(self):
        self.frontier = []
        self.explored = set()
        heappush(self.frontier, self.rootnode)
        self.solved = False
