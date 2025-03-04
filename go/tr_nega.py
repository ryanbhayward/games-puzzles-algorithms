# based on Jake Hennig's translation of Tromp's c program 
# solve 2x2 go, Tromp-Taylor rules, no self-capture, positional superko
# 2025: change abmmx to abnegamax

NSHOW  = 4  # max depth for displying search output
NMOVES = 4  # max number possible moves
PWRNMV = 16 # 2^NMOVES
CUT    = 1  # CUT 1 allows pruning, CUT 0 is minimax (2x2: too slow)

h = [0] * 256  # bitmap of positions in game history
nodes = [0] * 99  # number of nodes visited at each depth
ngames = 0  # number games scored

def show(n, black, white, alpha, beta, passed): #n: depth, b/w: bitsets
    '''2-line ascii rep'n of position'''
    print(f'{n} ({alpha},{beta})', 'pass' if passed else '')#if prev. move pass
    for j in range(NMOVES):
        if (j % 2 == 0):
            print(' ', end='')
        print('.*o#'[((black >> j) & 1) + 2 * ((white >> j) & 1)], end=' ')
        if (j == 1): print() 
        # 2x2: 1000 top-left, 0100 top-right, 0010 bottom-left, 0001 bottom-right

def visit(black, white): # mark position as visited
    h[black + 16 * white] = 1

def unvisit(black, white): # mark position as unvisited
    h[black + 16 * white] = 0

def visited(black, white): # has psn been visited?
    return h[black + 16 * white]

def owns(bb): # 2x2: does player own only 2 diagonally opposing corners?
    return bb == (1 | 8) or bb == (2 | 4)

popcnt = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]  
# number 1-bits in binary rep'n 0 to 15, used to count stones

def score(black, white): #calculate psn score
    global ngames
    ngames += 1 # counts number of times psn scored
    if (black == 0): return -4 if white else 0 # b no stones? w win or draw
    if (white == 0): return 4                  # w no stones? b win
    else: return popcnt[black] - popcnt[white] # score is stones difference

def xhasmove(black, white, move_index): # b has valid move?
    move = (1,2,4,8)[move_index] # get bin-rep'n of selected move
    if (black | white) & move or popcnt[black] == 3 or owns(white): # can you explain this?
      return False # no 
    newblack = black | move # update b psn: add stone
    newwhite = 0 if (newblack | white) == 15 or owns(newblack) else white # capture? update white
    return not visited(newblack, newwhite) # true if psn unvisited

def ohasmove(black, white, move_index): # see xhasmove for comments
    '''Check if white has a valid move'''
    #moves = [1, 2, 4, 8]
    move = (1,2,4,8)[move_index]
    if (black | white) & move or popcnt[white] == 3 or owns(black): return False 
    newwhite = white | move 
    newblack = 0 if (newwhite | black) == 15 or owns(newwhite) else black 
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
            newwhite = 0 if (newblack | white) == 15 or owns(newblack) else white
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
            newblack = 0 if (newwhite | black) == 15 or owns(newwhite) else black
            visit(newblack, newwhite) 
            s = xab(n + 1, newblack, newwhite, alpha, beta, 0)
            unvisit(newblack, newwhite) 
            if (s < beta):
                beta = s
                if (beta <= alpha and CUT): return beta 
    return beta

def main():
    s = 0
    c = xab(0, 0, 0, -4, 4, 0) # start alphabeta search from empty board
    for i, count in enumerate(nodes):
        s += count # total nodes visited
        if (count):
            print(f'{i}: {count}') # nodes visited at each depth

    print(f'total: {s}\nngames: {ngames}\nx wins by {c}') # nodes visited and game stats

if __name__ == '__main__':
    main()
