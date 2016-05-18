import argparse
from interface import Interface
from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.search.a_star import AStar
import sys

def main():
    """Main function to get and respond to user input."""
    puzzle = 'sliding_tile'
    solver = 'A*'
    if len(sys.argv) > 1:
	if sys.argv[1] in Interface.PUZZLES.keys():
	    puzzle = sys.argv[1]
	else:
	    print('Error: invalid puzzle name')
	    return
    if len(sys.argv) > 2:
	if sys.argv[2] in Interface.SOLVERS.keys():
	    solver = sys.argv[2]
	else:
	    print('Error: invalid solver name')
	    return
    interface = Interface(puzzle, solver)
    interface.prompt = '\n'
    interface.cmdloop()


if __name__ == "__main__":
    main()
