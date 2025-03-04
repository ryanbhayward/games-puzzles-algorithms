# Jake Hennig translated John Tromp's 2x2 ab-solver from c to python3,
# rbh translated from 2x2 go to trigo
# solve triangle-go, positional superko, Tromp-Taylor scoring, no self-capture
# Try pass-move before stone-moves (else too slow)
# TODO solve from arbitrary game-state

NSHOW = 5  # max depth for displying search output
NMOVES = 3  # max number possible moves
CUT = 1  # CUT 1 allows pruning otherwise, CUT 0 is minimax

h = [0] * 256  # bitmap of positions in game history
nodes = [0] * 99  # number of nodes visited at each depth
ngames = 0  # total  number games played

def show(n, black, white, alpha, beta, passed):
    '''Print 2-line ASCII representation of position'''
    print(f'{n} ({alpha},{beta})', 'pass' if passed else '', end='\n  ') # prints depth, alpha, beta, and if player passed turn */
    for j in range(3):
        print('.*o#'[((black >> j) & 1) + 2 * ((white >> j) & 1)], end=' ') # prints the board state (X - black, O - white) */
        if j == 1: print('\n   ', end='')
    print('\n')# 100 top-left, 010 top-right, 001 bottom

def visit(black, white):
    '''Mark the position as visited'''
    h[black + 8 * white] = 1

def unvisit(black, white):
    '''Mark the position as unvisited'''
    h[black + 8 * white] = 0

def visited(black, white):
    '''Check if the position has been visited'''
    return h[black + 8 * white]

popcnt = [0, 1, 1, 2, 1, 2, 2, 3]  # number of 1 bits in the binary representation of numbers from 0 to 7
# 000, 001, 010, 011, 100, 101, 110, 111
# Used to count stones of each player

def score(black, white):
    '''Calculate the score of the position'''
    global ngames
    ngames += 1 # counts number of games played
    if (black == 0): return -3 if white else 0 # black no stones? white wins (-3) unless white also no stones (draw 0)
    if (white == 0): return 3 # white no stones: black wins +3 
    else: return 0 # each have 1 stone

def xhasmove(black, white, move_index):
    '''Check if black has a valid move'''
    #moves = [1, 2, 4] # Different possible move decimal values
    move = (1,2,4)[move_index] # Get selected move
    if (black | white) & move or popcnt[black] == 2: return False # no 
    newblack = black | move # update black position
    newwhite = 0 if (newblack | white) == 7 else white # update white position after move
    return not visited(newblack, newwhite) # new position visited before?

def ohasmove(black, white, move_index): # see xhasmove for comments
    '''Check if white has a valid move'''
    #moves = [1, 2, 4]
    move = (1,2,4)[move_index]
    if (black | white) & move or popcnt[white] == 2: return False 
    newwhite = white | move 
    newblack = 0 if (newwhite | black) == 7 else black 
    return not visited(newblack, newwhite) 

def xab(n, black, white, alpha, beta, passed):
    '''Alpha-beta search for black's turn'''
    global nodes
    nodes[n] += 1 # nodes visited at this depth
    if n < NSHOW: show(n, black, white, alpha, beta, passed) # displays board state if within NSHOW depth

    # make pass move
    #   if previous opponent move was pass, position is terminal: calculate score
    #   otherwise continue search with parameter passed == 1
    s = score(black, white) if passed else oab(n + 1, black, white, alpha, beta, 1) 
    if (s > alpha):
        alpha = s
        if (alpha >= beta and CUT): return alpha # prune if score  > alpha and after update whether alpha  >= beta

    for i in range(NMOVES):  # try moves topleft, topright, btmleft, btmright
        if (xhasmove(black, white, i)):
            newblack, newwhite = black, white
            move = 1 << i
            newblack = black | move
            newwhite = 0 if (newblack | white) == 7 else white
            visit(newblack, newwhite) 
            s = oab(n + 1, newblack, newwhite, alpha, beta, 0)
            unvisit(newblack, newwhite) 
            if (s > alpha):
                alpha = s
                if (alpha >= beta and CUT): return alpha # prune if score > alpha and after update whether alpha >= beta
    return alpha

def oab(n, black, white, alpha, beta, passed): # see xab for comments
    '''Alpha-beta search for white's turn'''
    global nodes
    nodes[n] += 1 
    if (n < NSHOW): show(n, black, white, alpha, beta, passed) 

    s = score(black, white) if passed else xab(n + 1, black, white, alpha, beta, 1) 
    if (s < beta):
        beta = s
        if (beta <= alpha and CUT): return beta 

    for i in range(NMOVES):
        if (ohasmove(black, white, i)): 
            newblack, newwhite = black, white
            move = 1 << i
            newwhite = white | move
            newblack = 0 if (newwhite | black) == 7 else black
            visit(newblack, newwhite) 
            s = xab(n + 1, newblack, newwhite, alpha, beta, 0)
            unvisit(newblack, newwhite) 
            if (s < beta):
                beta = s
                if (beta <= alpha and CUT): return beta 
    return beta

def main():
    s = 0
    c = xab(0, 0, 0, -3, 3, 0) # start alphabeta search from empty board
    for i, count in enumerate(nodes):
        s += count # total nodes visited
        if (count):
            print(f'{i}: {count}') # nodes visited at each depth

    print(f'total: {s}\nngames: {ngames}\nx wins by {c}') # nodes visited and game stats

if __name__ == '__main__':
    main()
