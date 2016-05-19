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
        
    def search(self):
        """
        Perform A* until time_limit is reached.
        Returns a list of moves to reach the solution if it finds one, None
        if there is not solution, or False if the time limit is reached.
        """
        if self.solved:
            self.reset()
        start_time = time.time()
        if self.verbose:
            print('Starting A* search')
            self.print_verbose_statement(start_time)
            verbose_limit = 10
        
        while(time.time() - start_time < self.time_limit):
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
            
            current_node = heappop(self.frontier)
            if current_node.state.is_solved():
                if self.verbose:
                    print('Solution node found')
                    self.print_verbose_statement(start_time)
                self.solved = True
                return self.solution(current_node)
            
            self.explored.add(current_node.state.value())
            for move in current_node.state.valid_moves():
                new_state = current_node.state.copy()
                new_state.apply_move(move)
                child = Node(new_state, move, current_node, self.heuristic)
                in_frontier = self._update_frontier(child)
                if not (new_state.value() in self.explored or in_frontier):
                    heappush(self.frontier, child)
        
        if self.verbose:
            self.print_verbose_statement(start_time)
            print('The search timed out without finding a solution.')
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
    
    def reset(self):
        self.frontier = []
        self.explored = set()
        heappush(self.frontier, self.rootnode)
        self.solved = False