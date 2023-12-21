import time

# todo
# class hex_board
#    - n_rows, n_cols  <- can be different
#    - above can be set in __init__
#    - BLK, WHT  = 0, 1
#    - P1 = BLK  <- can be WHITE
#    - cells TOP, BTM, LFT, RGT
#    - sides ((TOP,BTm),(LFT, RGT))  <- can be switched
#    -        BLK sides  WHT sides  
#Owen Randall 2023
#H-search proof of concept prototype
#Not optimized or thoroughly tested

#edits RBH 2023
# fixed names: or_rule, and_rule  (originally misleading)
# carriers:    only show EMP cells (omit player's stones)
# sanity check: print color sets E B W, print board
# added some small tests

# bug: 5x5, black middle, doesn't find winning vc

# rbh: todo
# - vc.print: each pair output only once
# - semi: show key
# - unit tests
#-----------------------------

#Example 3x3 board with labeled points and sides:
#  N N N N
# W 0 1 2 E
#  W 3 4 5 E
#   W 6 7 8 E
#    S S S S

# only supports rhombus boards: same number rows, cols
# BRD_X * BRD_X board
BRD_X = 4                
BRD_SIZE = BRD_X * BRD_X

EMP, BLK, WHT = 0, 1, 2
COLORS = ('empty', 'black', 'white')

def opponent_name(s): 
    return COLORS[3 - s]

def player_name(s):   
    return COLORS[s]

def point_str(p):
    s = f'{p:2}'
    if s[1] == ' ': s = ' ' + s[0]
    return s

# return E/B/W cell sets of a dxd hex_board
def cell_sets(hb, d):
    nn = len(hb)
    assert(nn == d*d)
    sets = (set(), set(), set())
    for j in range(nn):
        sets[hb[j]].add(j)
    return sets

#check board boundaries
def E(p):
    return p % BRD_X != BRD_X-1

def W(p):
    return p % BRD_X != 0

def NE(p):
    return E(p) and p >= BRD_X

def NW(p):
    return p >= BRD_X

def SE(p):
    return p < BRD_SIZE - BRD_X

def SW(p):
    return W(p) and p < BRD_SIZE - BRD_X

#print hex board point-labels
def print_board_labels():
    print(' ',end='')
    for i in range(BRD_X+1):
        print(' n ',end='')
    print()
    for i in range(BRD_X):
        for j in range(i):
            print(' ',end='')
        print('w ',end='')
        for j in range(BRD_X):
            print(f'{i*BRD_X + j:2}' + ' ',end='')
        print(' e')
    print(' ' * (BRD_X-2),end='')
    for i in range(BRD_X+1):
        print('  s',end='')
    print('\n')

# print an actual dxd board hb
def show_board(hb, d):
    for r in range(d):
        print(r*' ', end='')
        for c in range(d):
            print('-*o'[hb[c+r*d]], end=' ')
        print()

#appropriate functions and offsets for checking adjacent points
adj_func_points = [(E, 1), (W, -1), (NE, -BRD_X+1), (NW, -BRD_X), (SE, BRD_X), (SW, BRD_X-1)]

#yields adjacent points of board which are in vals
def get_neighbors(p, vals, board):
    for f, offset in adj_func_points:
        if f(p) and board[p + offset] in vals:
            yield p + offset

# Virtual connection class
# Connects board points org to dest via carrier (set of board points)
class VC:
    def __init__(self, semi, org, dest, carrier):
        self.semi = semi #Is it a semi connection?
        self.org = org #Origin point
        self.dest = dest #Destination point
        self.carrier = carrier #Set of points that connect org to dest

    def mystr(self):
        return point_str(self.org) + (' semi ' if self.semi else ' full ') + str(self.carrier)

    def print(self):
        # str(self.dest) printed by caller
        print(self.mystr())

#Adds all adjacencies between player points or empty points
def add_initial_vcs(player_color, board):
    #vcs indexed by the destination point
    vcs = {}
    for i in range(BRD_SIZE):
        vcs[i] = []
    if player_color == BLK:
        for side in ['N', 'S']:
            vcs[side] = []
    else:
        for side in ['W', 'E']:
            vcs[side] = []

    #connections between points within the board
    for p, val in enumerate(board):
        if (val == player_color) or (val == EMP):
            for adj in get_neighbors(p, [EMP, player_color], board):
                vcs[adj].append(VC(False, p, adj, set()))
    
    #connections between the sides of the board and the points of the board
    if player_color == BLK:
        #north
        for p in range(BRD_X):
            if board[p] == player_color or board[p] == EMP:
                vcs[p].append(VC(False, 'N', p, set()))
                vcs['N'].append(VC(False, p, 'N', set()))
        #south
        for p in range(BRD_SIZE-BRD_X, BRD_SIZE):
            if board[p] == player_color or board[p] == EMP:
                vcs[p].append(VC(False, 'S', p, set()))
                vcs['S'].append(VC(False, p, 'S', set()))

    else:
        #west
        for p in range(0, BRD_SIZE, BRD_X):
            if board[p] == player_color or board[p] == EMP:
                vcs[p].append(VC(False, 'W', p, set()))
                vcs['W'].append(VC(False, p, 'W', set()))
        #east
        for p in range(BRD_X-1, BRD_SIZE, BRD_X):
            if board[p] == player_color or board[p] == EMP:
                vcs[p].append(VC(False, 'E', p, set()))
                vcs['E'].append(VC(False, p, 'E', set()))

    return vcs

#create a unique hash for a vc
def vc_hash(semi, org, dest, carrier):
    return str(semi) + str(org) + str(dest) + str(carrier)

def and_rule(vcs, board, hashes, shared_color, create_semis):
    new_vcs = []
    #iterate over all destination points
    for p in vcs:
        #only consider shared destinations of the specified color
        if (type(p) == str) or (board[p] != shared_color):
            continue
        for a in vcs[p]:
            #only consider full vcs
            if a.semi:
                continue
            for b in vcs[p]:
                #ensure both vcs have a different origin
                if b.semi or (b.org == a.org):
                    continue
                #create new carrier: union existing carriers and shared destination
                new_carrier = a.carrier.union(b.carrier)
                # rbh: if p==EMP, it is also added to the carrier
                if board[p] == EMP: new_carrier.add(p)
                #ensure vc not yet created
                if vc_hash(create_semis, a.org, b.org, new_carrier) in hashes:
                    continue
                #ensure no existing full vc joining same points as new semi vc
                #ensure no existing vc with proper subset of new carrier
                invalid = False
                for c in vcs[b.org]:
                    if c.org == a.org and \
                       (not c.semi and \
                       (create_semis or c.carrier.issubset(new_carrier))):
                        invalid = True
                        break
                if invalid:
                    continue
                #Add hashes and new vcs
                hashes.add(vc_hash(create_semis, a.org, b.org, new_carrier))
                hashes.add(vc_hash(create_semis, b.org, a.org, new_carrier))
                new_vcs.append(VC(create_semis, a.org, b.org, new_carrier))
                new_vcs.append(VC(create_semis, b.org, a.org, new_carrier))
    
    for vc in new_vcs:
        vcs[vc.dest].append(vc)

    #Return whether any new vcs were found
    return len(new_vcs) > 0

def or_rule(vcs, board, hashes, empty_points):
    new_vcs = []
    #iterate over all destination points
    for p in vcs:
        for a in vcs[p]:
            #consider only semis
            if not a.semi:
                continue
            for b in vcs[p]:
                #ensure vcs same origin and non-intersecting carriers 
                if not b.semi or a.org != b.org or a.carrier.intersection(b.carrier):
                    continue
                #create the new carrier as the union of the existing carriers
                new_carrier = a.carrier.union(b.carrier)
                #ensure vc not yet created
                if vc_hash(False, a.org, a.dest, new_carrier) in hashes:
                    continue
                #ensure no existing full vc with subset carrier
                found_subset = False
                for c in vcs[a.dest]:
                    if not c.semi and c.org == a.org and c.carrier.issubset(new_carrier):
                        found_subset = True
                        break
                if found_subset:
                    continue
                #add hashes and new vcs
                hashes.add(vc_hash(False, a.org, a.dest, new_carrier))
                hashes.add(vc_hash(False, a.dest, a.org, new_carrier))
                new_vcs.append(VC(False, a.org, a.dest, new_carrier))
                new_vcs.append(VC(False, a.dest, a.org, new_carrier))

    for vc in new_vcs:
        vcs[vc.dest].append(vc)

    return len(new_vcs) > 0

def weird(vc,x,y):
    return vc.org==x and vc.dest==y or vc.org==y and vc.dest==x

def remove_redundant_vcs(vcs):
    for p in vcs:
        to_remove = []
        for a in vcs[p]:
            for b in vcs[p]:
                # removed this: a.semi and not b.semi
                if a != b and a.org == b.org and \
                    a.semi == b.semi and b.carrier.issubset(a.carrier):
                    to_remove.append(a)
                    if weird(a,11,'N'): 
                        print('this is why we are removing')
                        b.print()
                    break
        for vc in to_remove:
            if weird(vc,11,'N'):
                print('WEIRD')
                vc.print()
            vcs[p].remove(vc)

def mustplay(player_color, connections):
    print('\n ***', player_name(player_color), end=' ')
    mp = set(range(BRD_SIZE))
    sides = ('N','S') if (player_color == BLK) else ('W','E')
    for vc in connections[sides[0]]:
        if vc.org == sides[1]:
            if not vc.semi:
                print(' winning vc !!! *** ')
                vc.print()
                return
            else:
                mp &= vc.carrier
    print('has not yet won')
    print(' ***', opponent_name(player_color), 'mustplay: ', end='')
    print(mp)

def print_all(conns):
    for p in conns:
        print('\ndest', p)
        L = []
        for vc in conns[p]:
            L.append(vc.mystr())
        L.sort()
        for x in L:
            print(x)

def print_side_to_side(conns, player):
    sides = ('N','S') if player == BLK else ('W','E')
    for j in range(2):
        print('\n vcs/scs with dest ', sides[j])
        for vc in conns[sides[j]]:
            vc.print()

def h_search(player_color, board):
    #print('Board points:')
    print_board_labels()

    start_time = time.time()
    #Create empty points set
    empty_points = set()
    for i in range(BRD_SIZE):
        if board[i] == EMP:
            empty_points.add(i)
    #Create initial connections
    connections = add_initial_vcs(player_color, board)
    #Iterate the or and and rules until no new vcs are found
    any_changes = True
    vc_hashes = set()
    while any_changes:
        #Standard AND rule, create semi connections
        any_changes = and_rule(connections, board, vc_hashes, EMP, True) 
        #AND rule except shared destination point is a player stone, create full connections
        any_changes = and_rule(connections, board, vc_hashes, player_color, False) or any_changes
        #OR rule, create full connections
        any_changes = or_rule(connections, board, vc_hashes, empty_points) or any_changes
        #Remove any connections which are supersets of other equivalent connections, or are semi connections for fully connected points
        remove_redundant_vcs(connections)

    end_time = time.time()

    print_all(connections)
    #print_side_to_side(connections, player_color)
    mustplay(player_color, connections)

    print('\nTime taken:', end_time - start_time)

#init board
hex_board = [0 for i in range(BRD_SIZE)]
#You can set stones by point index here for example:
#  hex_board[0] = BLK
#  hex_board[3] = WHT

def analyze(seq):
    if len(seq) == 0:
        h_search(WHT, hex_board)
        return
    for move in seq:
        hex_board[move[1]] = move[0]
    h_search(move[0], hex_board)
    show_board(hex_board, BRD_X)

# proof tree for 1.B[a3] lose
# * indicates fillin
# B  W  B  W  B  W  B
# 8 12  9 13 
#       7 14*

# proof tree for 1.B[a4] win
# * indicates fillin
#  B  W  B  W  B  W  B
# 12  2  4*
#     9  6*

#4x4
#m = [[BLK,8], [WHT,12], [BLK,7], [WHT,14], [WHT,15], [WHT,11]]
#5x5
#m = [[BLK,12], [WHT,3], [BLK,6]]
m = [[BLK,12]]
analyze(m)
