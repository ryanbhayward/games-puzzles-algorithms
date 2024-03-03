# Created by Luke Schultz
# Fall 2022, Winter 2023, Spring 2023, Summer 2023, Fall 2023
# Written with the help of GitHub Copilot

import hex_game0
import hex_game1
import hex_game2
from hex_game0 import BLACK, WHITE, BLANK
import mcts0
import mcts1

size = 6
previous_game = None
boardversion = 2  # 0 or 1 or 2
mctsversion = 1  # 0 or 1

boardversions = [hex_game0.Hex0, hex_game1.Hex1, hex_game2.Hex2]
mctsversions = [mcts0.Mcts0, mcts1.Mcts1]


def coord_to_move(coord: str) -> list:
    """convert coord in the form a1 to list index"""
    assert(ord(coord[0]) >= 97 and ord(coord[0]) <= 122)
    col = ord(coord[0]) - 97
    if col >= 9:
        col -= 1
    row = int(coord[1:])-1

    return (row+1) * (size+2) + col+1


def command_loop(game):
    global size
    global previous_game
    global boardversion
    global mctsversion

    command = None
    while command != "exit" and command != "quit" and command != "q":
        print("= ", end="")
        command = input().lower()

        if command.replace(" ", "") == "":
            continue

        args = command.lower().split()
        if args[0] == "x" or args[0] == "o" or args[0] == ".":
            try:
                move = coord_to_move(args[1])
                previous_game = game.copy()
                if args[0] == "x":
                    game.play_move(move, BLACK)
                elif args[0] == "o":
                    game.play_move(move, WHITE)
                elif args[0] == ".":
                    game.clear_move(move)
                print(str(game))
            except:
                print("invalid coordinate")
                continue
        elif args[0] == "show":
            print(str(game))
        elif args[0] == "size":
            global size
            try:
                size = int(args[1])
            except:
                print("invalid size")
                continue
            previous_game = game.copy()
            game = boardversions[boardversion](size)
            print(str(game))
        elif args[0] == "reset":
            previous_game = game.copy()
            game = boardversions[boardversion](size)
            print(str(game))
        elif args[0] == "undo":
            game = previous_game
            print(str(game))
        elif args[0] == "gameversion":
            try:
                assert(0 <= int(args[1]) <= 2)
                gameversion = int(args[1])
            except:
                print("invalid game version, see readme for list of versions")
                continue
            previous_game = game.copy()
            game = boardversions[gameversion](size)
            print(str(game))
        elif args[0] == "mctsversion":
            try:
                assert(0 <= int(args[1]) <= 1)
                mctsversion = int(args[1])
            except:
                print("invalid mcts version, see readme for list of versions")
                continue
        elif args[0] == "mcts":
            try:
                assert(args[1] == "x" or args[1] == "o")
            except:
                print("invalid player, see readme for list of players")
                continue

            previous_game = game.copy()

            if args[1] == "x":
                mcts = mctsversions[mctsversion](game, BLACK)
                move = mcts.monte_carlo_tree_search()
                print("number of simulations performed:", mcts.root_node.sims)
                game.play_move(move, BLACK)
            elif args[1] == "o":
                previous_game = game.copy()
                mcts = mctsversions[mctsversion](game, WHITE)
                move = mcts.monte_carlo_tree_search()
                print("number of simulations performed:", mcts.root_node.sims)
                game.play_move(move, WHITE)

            print(str(game))
        elif args[0] != "exit" and args[0] != "quit" and args[0] != "q":
            print("invalid command, see readme for list of commands")


if __name__ == "__main__":
    game = boardversions[boardversion](size)
    command_loop(game)
