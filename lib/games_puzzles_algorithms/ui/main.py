from interface import Interface
import sys

def main():
    """Main function to get and respond to user input."""
    puzzle = 'solvable_sliding_tile'
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