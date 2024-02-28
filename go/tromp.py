# Jake Hennig 2024
# translation of John Tromp's c program to python3
# solve 2x2 go with area rules and positional superko

# Note that suicide is not possible in this case
# Trying moves before passes slows search dramatically

NSHOW = 4  # max depth for displying search output
NMOVES = 4  # max number possible moves
CUT = 1  # CUT 1 allows pruning otherwise, CUT 0 is minimax

h = [0] * 256  # bitmap of positions in game history
nodes = [0] * 99  # number of nodes visited at each depth
ngames = 0  # total  number games played

def show(n, black, white, alpha, beta, passed):
    """Print 2-line ASCII representation of position"""
    print(f"{n} ({alpha},{beta})", "pass" if passed else "") # prints depth, alpha, beta, and if player passed turn */
    for i in range(4):
        if (i % 2 == 0):
            print(" ", end="")
        print(".XO#"[((black >> i) & 1) + 2 * ((white >> i) & 1)], end=" ") # prints the board state (X - black, O - white) */
        if (i & 1):
            print() # place new line after every two characters - 2x2 board */
# 1000 top-left, 0100 top-right, 0010 bottom-left, 0001 bottom-right

def visit(black, white):
    """Mark the position as visited"""
    h[black + 16 * white] = 1

def unvisit(black, white):
    """Mark the position as unvisited"""
    h[black + 16 * white] = 0

def visited(black, white):
    """Check if the position has been visited"""
    return h[black + 16 * white]

def owns(bb):
    """Check if one player has both corners of the board (control over it)"""
    return bb == (1 | 8) or bb == (2 | 4)

popcnt = [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]  # number of 1 bits in the binary representation of numbers from 0 to 15
# 0000, 0001, 0010, 0011, 0100, 0101... 1110, 1111
# Used to count stones of each player

def score(black, white):
    """Calculate the score of the position"""
    global ngames
    ngames += 1 # counts number of games played
    if (black == 0): return -4 if white else 0 # black no stones? white wins (-4) unless white also no stones (draw 0)
    if (white == 0): return 4 # white no stones: black wins +4 */
    else: return popcnt[black] - popcnt[white] # score is stones difference

def xhasmove(black, white, move):
    """Check if black has a valid move"""
    move = 1 << move # get move binary representation
    if (black | white) & move or popcnt[black] == 3 or owns(white): return False # no 
    newblack = black | move # update black position
    newwhite = 0 if (newblack | white) == 15 or owns(newblack) else white # update white position after move
    return not visited(newblack, newwhite) # new position visited before?

def ohasmove(black, white, move): # see xhasmove for comments
    """Check if white has a valid move"""
    move = 1 << move 
    if (black | white) & move or popcnt[white] == 3 or owns(black): return False 
    newwhite = white | move 
    newblack = 0 if (newwhite | black) == 15 or owns(newwhite) else black 
    return not visited(newblack, newwhite) 

def xab(n, black, white, alpha, beta, passed):
    """Alpha-beta search for black's turn"""
    global nodes
    nodes[n] += 1 # nodes visited at this depth
    if n < NSHOW: show(n, black, white, alpha, beta, passed) # displays board state if within NSHOW depth

    # if opponent passed and we now pass, terminal position so calculate score, otw continue search
    s = score(black, white) if passed else oab(n + 1, black, white, alpha, beta, 1) 
    if (s > alpha):
        alpha = s
        if (alpha >= beta and CUT): return alpha # prune if score  > alpha and after update whether alpha  >= beta

    for i in range(NMOVES): # loop through possible moves
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
    """Alpha-beta search for white's turn"""
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
            print(f"{i}: {count}") # nodes visited at each depth

    print(f"total: {s}\nngames: {ngames}\nx wins by {c}") # nodes visited and game stats

if __name__ == "__main__":
    main()
