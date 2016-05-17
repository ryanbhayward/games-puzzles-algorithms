from cmd import Cmd
from games_puzzles_algorithms.search.a_star import AStar
from games_puzzles_algorithms.search.breadth_first_search import BreadthFirstSearch
from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.puzzles.maze_puzzle import MazePuzzle


class Interface(Cmd):
    """
    Generalized interface for puzzles and solvers.
    """

    SOLVERS = {"A*": AStar, "breadth_first_search": BreadthFirstSearch}
    PUZZLES = {
        SlidingTilePuzzle.NAME: SlidingTilePuzzle,
        MazePuzzle.NAME: MazePuzzle
    }

    def __init__(self, puzzle, solver, heuristic=None):
        """
        Initialize the interface.
        puzzle, solver, and heuristic are all strings giving the names of
        a puzzle in PUZZLES, a search algorithm in SOLVERS, and a valid
        heuristic for puzzle.
        """
        Cmd.__init__(self)
        self.time_limit = 30

        if puzzle == SlidingTilePuzzle.NAME:
            self.size = 3
            if solver == "A*" and heuristic is None:
                heuristic = "manhattan distance"
            self.heuristic = heuristic
            self.puzzle_name = self.PUZZLES[puzzle]
            self.puzzle = self.puzzle_name(self.size)

            if solver in self.SOLVERS:
                self.solver_name = self.SOLVERS[solver]
                self.solver = self.solver_name(self.puzzle, self.time_limit, heuristic)
        elif puzzle == MazePuzzle.NAME:
            self.width = 5
            self.height = 5
            self.puzzle_name = self.PUZZLES[puzzle]
            self.puzzle = MazePuzzle(self.width, self.height)
        else:
            raise Exception("Specified puzzle " + puzzle + " is not defined!")

        print(puzzle)
        self.do_show_puzzle("")
        print("Type 'help' for a list of commands.")

    def do_quit(self, args):
        """Exit the program."""
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
        print("is_solved")

    def do_set_size(self, args):
        """Set the size of the puzzle problem."""
        if self.puzzle_name.NAME == SlidingTilePuzzle.NAME:
            try:
                size = int(args)
            except ValueError:
                print("Error: invalid size")
            if size < 1:
                print("Error: invalid size")
            self.size = size
            self.do_new_puzzle("")
        elif self.puzzle_name.NAME == MazePuzzle.NAME:
            sizes = args.split(" ")
            if len(sizes) != 2:
                print("Error: invalid sizes. Expected 2 numbers")
                return
            try:
                self.width = int(sizes[0])
                self.height = int(sizes[1])
            except ValueError:
                print("Error: invalid sizes. Expected 2 numbers")
                return
            self.size = sizes
            self.do_new_puzzle("")

    def do_set_time(self, args):
        """Set the time limit for search."""
        if self.puzzle_name.NAME == SlidingTilePuzzle.NAME:
            try:
                time = int(args)
            except ValueError:
                print("Error: invalid time")
            if time < 0:
                print("Error: invalid time")
            self.time_limit = time
            self.solver = self.solver_name(self.puzzle, time, self.heuristic)
        elif self.puzzle_name.NAME == MazePuzzle.NAME:
            # todo: set maze time for solver
            print(args)

    def do_show_puzzle(self, args):
        """Print a string representation of the puzzle."""
        print(self.puzzle)

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

    def do_get_moves(self, args):
        """Print a list of all valid moves in the current state."""
        print(", ".join(self.puzzle.str_moves(self.puzzle.valid_moves())))

    def do_search(self, args):
        """
        Search for a solution and print the moves to reach it if one is found.
        """
        if self.puzzle_name.NAME == SlidingTilePuzzle.NAME:
            result = self.solver.search()
            if result is None:
                print("The puzzle has no solution.")
            elif not result:
                print("The search timed out.""")
                print(str(self.solver.num_nodes_generated()) + " nodes were generated")
        elif self.puzzle_name.NAME == MazePuzzle.NAME:
            # todo set maze do search
            print(args)

    def do_new_puzzle(self, args):
        """Generate a new puzzle of the same size as the current one"""
        seed = None
        if len(args) > 0:
            try:
                seed = int(args)
            except ValueError:
                print("Error: invalid seed")
        if self.puzzle_name.NAME == SlidingTilePuzzle.NAME:
            self.puzzle = self.puzzle_name(self.size, seed)
            self.solver = self.solver_name(self.puzzle, self.time_limit, self.heuristic)
        elif self.puzzle_name.NAME == MazePuzzle.NAME:
            self.puzzle = self.puzzle_name(self.width, self.height, seed)
            # todo: setup maze solver
        print(self.puzzle.NAME)
        print(self.puzzle)

    def do_set_heuristic(self, args):
        """Set the heuristic for the search."""
        if args in self.puzzle_name.HEURISTICS:
            self.heuristic = args
            self.solver = self.solver_name(self.puzzle, self.time_limit, self.heuristic)

    def do_is_solved(self, args):
        """Print True if the puzzle is solved. False otherwise."""
        print(self.puzzle.is_solved())
