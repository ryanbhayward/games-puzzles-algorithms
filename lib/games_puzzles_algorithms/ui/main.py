import argparse

from interface import Interface


def main():
    """Main function to get and respond to user input."""
    parser = argparse.ArgumentParser('Interact with puzzles and solvers.')
    parser.add_argument('puzzle', choices=Interface.PUZZLES.keys(),
                        default='solvable_sliding_tile', nargs='?')
    parser.add_argument('solver', choices=Interface.SOLVERS.keys(),
                        default='A*', nargs='?')

    args = parser.parse_args()

    interface = Interface(args.puzzle, args.solver)
    interface.prompt = '\n'
    interface.cmdloop()


if __name__ == "__main__":
    main()
