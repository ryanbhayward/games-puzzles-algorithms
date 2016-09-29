from cmd import Cmd
# TODO Ideally this module shouldn't know about the modules in search.
#   Instead, the executable that uses this interface should hold that
#   information and only pass in the necessary instances, like
#   the games CLI module.
from games_puzzles_algorithms.search.a_star import AStar
from games_puzzles_algorithms.search.breadth_first_search import BreadthFirstSearch
from games_puzzles_algorithms.search.depth_first_search import DepthFirstSearch
from .sliding_tile_puzzle import SlidingTilePuzzle
from .solvable_sliding_tile_puzzle import SolvableSlidingTilePuzzle

class Interface(Cmd):
    """
    Generalized interface for puzzles and solvers.
    """

    SOLVERS = {"A*": AStar, "bfs": BreadthFirstSearch}
    PUZZLES = {"sliding_tile": SlidingTilePuzzle,
               "sst": SolvableSlidingTilePuzzle}

    def __init__(self, puzzle, solver, heuristic=None):
        """
        Initialize the interface.
        puzzle, solver, and heuristic are all strings giving the names of
        a puzzle in PUZZLES, a search algorithm in SOLVERS, and a valid
        heuristic for puzzle.
        """
        Cmd.__init__(self)
        self.time_limit = 30
        self.verbose = True

        self.size1 = 3
        self.size2 = 3
        if solver == "A*" and heuristic is None:
            heuristic = "manhattan distance"
        self.heuristic = heuristic
        if puzzle in self.PUZZLES:
            self.puzzle_name = self.PUZZLES[puzzle]
            self.puzzle = self.puzzle_name(size1=self.size1, size2=self.size2)

        if solver in self.SOLVERS:
            self.solver_name = self.SOLVERS[solver]
            self.new_solver()
        self.solver.set_verbose(self.verbose)

    def new_solver(self):
        """Create a new solver based on the current attribute values."""
        if self.solver_name == self.SOLVERS['A*']:
            self.solver = self.solver_name(self.puzzle, self.time_limit,
                                           self.heuristic)
        else:
            self.solver = self.solver_name(self.puzzle, self.time_limit)

    def do_quit(self, args):
        """Exit the program."""
        return True

    def do_EOF(self, args):
        """EOF reached, exit the program."""
        return True

    def do_help(self, args):
        """Print a list of available commands."""
        print("The available commands are:")
        print("quit")
        print("help")
        print("set_size")
        print("set_time")
        print("show_puzzle")
        print("move")
        print("get_moves")
        print("search")
        print("new_puzzle")
        print("set_heuristic")
        print("set_solver")
        print("is_solved")
        print("verbose")

    def do_set_size(self, args):
        """
        Set the size of the puzzle problem.
        args should be one or two positive numbers separated by a space.
        The first number is the number of rows, and the second if given is the
        number of columns. Otherwise the number of columns and rows are equal.
        """
        try:
            args = args.split(' ')
            size1 = int(args[0])
            if len(args) > 1:
                size2 = int(args[1])
            else:
                size2 = size1
        except ValueError:
            print("Error: invalid size")
            return
        if size1 < 1 or size2 < 1:
            print("Error: invalid size")
            return

        self.size1 = size1
        self.size2 = size2
        self.do_new_puzzle("")

    def do_set_time(self, args):
        """Set the time limit for search."""
        try:
            time = int(args)
        except ValueError:
            print("Error: invalid time")
            return
        if time < 0:
            print("Error: invalid time")
            return
        self.solver.set_time(time)

    def do_show_puzzle(self, args):
        """Print a string representation of the puzzle."""
        print(self.puzzle)
        print(self.heuristic)
        print('time limit', self.solver.time_limit)
        if self.verbose: print('verbose')
        else: print('not verbose')

    def do_move(self, args):
        """Apply the move given by args to the puzzle."""
        if args not in self.puzzle.str_moves(self.puzzle.valid_moves()):
            print("Error: " + args + " is not a valid move in this state.")
            return
        self.puzzle.apply_move(args)
        print(self.puzzle)
        if self.puzzle.is_solved():
            print("Congratulations! You solved the puzzle.")
            print("Generating a new puzzle...")
            self.do_new_puzzle("")
        # Workaround fix for no search available after maze move
        self.solver = self._instantiate_solver()

    # noinspection PyUnusedLocal
    def do_get_moves(self, args):
        """Print a list of all valid moves in the current state."""
        print(", ".join(self.puzzle.str_moves(self.puzzle.valid_moves())))

    # noinspection PyUnusedLocal
    def do_search(self, args):
        """
        Search for a solution and print the moves to reach it if one is found.
        """
        result = self.solver.search(self.verbose)
        if result is None:
            print("The puzzle has no solution.")
        elif not result:
            print("The search timed out.""")
            print(str(self.solver.num_nodes_generated()) + " nodes were "
                  "generated")
        else:
            print(', '.join(self.puzzle.str_moves(result)))

    def do_new_puzzle(self, args):
        """Generate a new puzzle of the same size as the current one"""
        seed = None
        if len(args) > 0:
            try:
                seed = int(args)
            except ValueError:
                print("Error: invalid seed")
                return

        self.puzzle = self.puzzle_name(self.size1, seed, self.size2)
        self.new_solver()

    def do_set_heuristic(self, args):
        """Set the heuristic for the search."""
        if args in self.puzzle_name.HEURISTICS:
            self.heuristic = args
            self.new_solver()

    def do_is_solved(self, args):
        """Print True if the puzzle is solved. False otherwise."""
        print(self.puzzle.is_solved())

    def do_verbose(self, args):
        """
        Set the verbosity of the output.
        args should be True or False or t or f as a string.
        """
        if args[0].lower() == 't':
            self.verbose = True
        elif args[0].lower() == 'f':
            self.verbose = False
        else:
            print('Error: invalid argument, should be t or f')
            return

        self.solver.set_verbose(self.verbose)
