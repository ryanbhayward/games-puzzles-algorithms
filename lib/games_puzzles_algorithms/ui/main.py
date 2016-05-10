from interface import Interface
from games_puzzles_algorithms.puzzles.sliding_tile_puzzle import SlidingTilePuzzle
from games_puzzles_algorithms.search.a_star import AStar

def main():
    """Main function to get and respond to user input."""
    interface = Interface("sliding_tile", "A*")
    interface.prompt = "\n"
    interface.cmdloop()
    
if __name__ == "__main__":
	main()