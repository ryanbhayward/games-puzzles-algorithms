# Python program to solve 2x2 go with area rules and positional superko
# translation of John Tromp's program by Jake Hennig 2024

# Note that suicide is not possible in this case
# Trying moves before passes slows search dramatically

NSHOW = 4  # the max depth that output of searches is displayed
NMOVES = 4  # of possible moves player can make
CUT = 1  # CUT set to 1 allows for pruning otherwise if set to 0 it just uses minimax

h = [0] * 256  # bitmap of positions in game history
nodes = [0] * 99  # number of nodes visited at each depth
ngames = 0  # total  # of games played

def show(n, black, white, alpha, beta, passed):
    """Print 2-line ASCII representation of position"""
    print(f"{n} ({alpha},{beta})", "pass" if passed else "") # prints current depth, alpha, beta, and if player passed turn */
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
    if (black == 0):
        return -4 if white else 0 # black has no stones, white wins (-4), unless white also has no pieces left then it's a draw (0)
    if (white == 0):
        return 4 # white has no pieces left, black wins (+4) */
    else:
        return popcnt[black] - popcnt[white] # calculates score based on the number of pieces each player has

def xhasmove(black, white, move):
    """Check if black has a valid move"""
    move = 1 << move # get binary representation of the move
    if (black | white) & move or popcnt[black] == 3 or owns(white): # checks if move is legal for black
        return False # move impossible
    newblack = black | move # updates black's position after move
    newwhite = 0 if (newblack | white) == 15 or owns(newblack) else white # updated white's position after move
    return not visited(newblack, newwhite) # checks if new position has been visited before

def ohasmove(black, white, move):
    """Check if white has a valid move"""
    move = 1 << move # get binary representation of the move
    if (black | white) & move or popcnt[white] == 3 or owns(black): # checks if move is legal for white
        return False # move impossible
    newwhite = white | move # updates white's position after move
    newblack = 0 if (newwhite | black) == 15 or owns(newwhite) else black # updates black's position after move
    return not visited(newblack, newwhite) # checks if new position has been visited before

def xab(n, black, white, alpha, beta, passed):
    """Alpha-beta search for black's turn"""
    global nodes
    nodes[n] += 1 # counts nodes visited at this depth
    if n < NSHOW:
        show(n, black, white, alpha, beta, passed) # displays board state if within NSHOW depth

    s = score(black, white) if passed else oab(n + 1, black, white, alpha, beta, 1) # calculates score or explores further for black's turn
    if (s > alpha):
        alpha = s
        if (alpha >= beta and CUT):
            return alpha # prune if current score (s) is > than alpha, and after updating alpha it's still >= to beta

    for i in range(NMOVES): # loop through possible moves
        if (xhasmove(black, white, i)): # checks if the move is possible
            newblack, newwhite = black, white
            move = 1 << i
            newblack = black | move
            newwhite = 0 if (newblack | white) == 15 or owns(newblack) else white
            visit(newblack, newwhite) # visits the new position
            s = oab(n + 1, newblack, newwhite, alpha, beta, 0)
            unvisit(newblack, newwhite) # unvisit the new position
            if (s > alpha):
                alpha = s
                if (alpha >= beta and CUT):
                    return alpha # prune if current score (s) is > than alpha, and after updating alpha it's still >= to beta
    
    return alpha

def oab(n, black, white, alpha, beta, passed):
    """Alpha-beta search for white's turn"""
    global nodes
    nodes[n] += 1 # counts nodes visited at this depth
    if (n < NSHOW):
        show(n, black, white, alpha, beta, passed) # displays board state if within NSHOW depth

    s = score(black, white) if passed else xab(n + 1, black, white, alpha, beta, 1) # calculates score or explores further for white's turn
    if (s < beta):
        beta = s
        if (beta <= alpha and CUT):
            return beta # prune if current score (s) < than beta, and after updating beta it's still <= to alpha

    for i in range(NMOVES): # loop through possible moves
        if (ohasmove(black, white, i)): # checks if the move is possible
            newblack, newwhite = black, white
            move = 1 << i
            newwhite = white | move
            newblack = 0 if (newwhite | black) == 15 or owns(newwhite) else black
            visit(newblack, newwhite) # visits the new position
            s = xab(n + 1, newblack, newwhite, alpha, beta, 0)
            unvisit(newblack, newwhite) # unvisit the new position
            if (s < beta):
                beta = s
                if (beta <= alpha and CUT):
                    return beta # prune if current score (s) < than beta, and after updating beta it's still <= to alpha
    
    return beta

def main():
    s = 0
    c = xab(0, 0, 0, -4, 4, 0) # starts the alpha-beta search from the initial position
    for i, count in enumerate(nodes):
        s += count # count total nodes visited
        if (count):
            print(f"{i}: {count}") # prints nodes visited at each depth

    print(f"total: {s}\nngames: {ngames}\nx wins by {c}") # prints total nodes visited and game stats

if __name__ == "__main__":
    main()
