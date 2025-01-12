# Written by Luke Schultz
# Winter 2023

import hex_game0
import hex_game1
import hex_game1_1
import hex_game2
import mcts0
import mcts1

from hex_game0 import ( BLACK, WHITE )

games = [hex_game0.Hex, hex_game1.Hex1, hex_game1_1.Hex1_1, hex_game2.Hex2]

def sim_count_test(average=5, size=8):
    averages = [0] * len(games)

    for i in range(len(games)):
        game = games[i](size)
        print(type(game))
        for j in range(average):
            mcts = mcts0.Mcts(game, BLACK)
            print(type(game.board))
            mcts.monte_carlo_tree_search()
            averages[i] += mcts.root_node.sims
        averages[i] /= average

    print(averages)

def play(game_version1, game_version2, size, num_games):
    win_count = [0, 0]

    for i in range(num_games):
        if i % 2 == 0:
            game1 = game_version1(size)
            game2 = game_version2(size)
        else:
            game1 = game_version2(size)
            game2 = game_version1(size)
        
        print("game1: ", type(game1))
        print("game2: ", type(game2))
        
        won = False
        player = 1
        while not won:
            if player == 1:
                mcts = mcts0.Mcts(game1, BLACK)
                move = mcts.monte_carlo_tree_search()
                won = game1.play_move(move)
                game2.play_move(move)
                print(str(game1))
                print(str(game2))

                if won and i % 2 == 0:
                    win_count[0] += 1
                elif won and i % 2 == 1:
                    win_count[1] += 1
            else:
                mcts = mcts0.Mcts(game2, BLACK)
                move = mcts.monte_carlo_tree_search()
                won = game2.play_move(move)
                game1.play_move(move)
                print(str(game1))

                if won and i % 2 == 0:
                    win_count[1] += 1
                elif won and i % 2 == 1:
                    win_count[0] += 1    
            
            player = 3 - player  # alternate player
    print(win_count)

def play_mcts(game_version, size, num_games):
    win_count = [0, 0]

    for i in range(num_games):
        game = game_version(size)
    
        won = False
        player = 2 - (i % 2)
        while not won:
            if player == 1:
                mcts = mcts0.Mcts(game, BLACK)
                move = mcts.monte_carlo_tree_search()
                won = game.play_move(move, BLACK)
                print(str(game))

                if won:
                    win_count[0] += 1
            else:
                mcts = mcts1.Mcts(game, WHITE)
                move = mcts.monte_carlo_tree_search()
                won = game.play_move(move, WHITE)
                print(str(game))

                if won:
                    win_count[1] += 1
            
            player = 3 - player  # alternate player
    
    print(win_count)

#sim_count_test(5, 8)
#play(games[0], games[1], 8, 6)
play_mcts(games[3], 6, 6)