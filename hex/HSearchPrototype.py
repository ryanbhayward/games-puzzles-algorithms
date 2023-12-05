import time
#H-search proof of concept prototype
#Not optimized or thoroughly tested

#Example 3x3 board with labeled points and sides:
#  N N N N
# W 0 1 2 E
#  W 3 4 5 E
#   W 6 7 8 E
#    S S S S

#Change to desired board size (only supports square boards)
BOARD_X = 3
BOARD_SIZE = BOARD_X * BOARD_X

EMPTY = 0
BLACK = 1
WHITE = 2

#check board boundaries
def E(p):
    return p % BOARD_X != BOARD_X-1

def W(p):
    return p % BOARD_X != 0

def NE(p):
    return E(p) and p >= BOARD_X

def NW(p):
    return p >= BOARD_X

def SE(p):
    return p < BOARD_SIZE - BOARD_X

def SW(p):
    return W(p) and p < BOARD_SIZE - BOARD_X

#Prints a board with labeled points and sides
def print_labeled_board():
    print(" ",end="")
    for i in range(BOARD_X+1):
        print("N ",end="")
    print()
    for i in range(BOARD_X):
        for j in range(i):
            print(" ",end="")
        print("W ",end="")
        for j in range(BOARD_X):
            print(str(i*BOARD_X + j) + " ",end="")
        print("E")
    for i in range(BOARD_X):
        print(" ",end="")
    for i in range(BOARD_X+1):
        print("S ",end="")
    print()

#appropriate functions and offsets for checking adjacent points
adj_func_points = [(E, 1), (W, -1), (NE, -BOARD_X+1), (NW, -BOARD_X), (SE, BOARD_X), (SW, BOARD_X-1)]

#yeilds adjacent points of board which are in vals
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

    def print(self):
        print("Semi: " + str(self.semi) + ", Org: " + str(self.org) + ", Dest: " + str(self.dest) + ", Carrier: " + str(self.carrier))

#Adds all adjacencies between player points or empty points
def add_initial_vcs(player_color, board):
    #vcs indexed by the destination point
    vcs = {}
    for i in range(BOARD_SIZE):
        vcs[i] = []
    if player_color == BLACK:
        for side in ["N", "S"]:
            vcs[side] = []
    else:
        for side in ["W", "E"]:
            vcs[side] = []

    #connections between points within the board
    for p, val in enumerate(board):
        if val == player_color or val == EMPTY:
            for adj in get_neighbors(p, [EMPTY, player_color], board):
                vcs[adj].append(VC(False, p, adj, set()))
    
    #connections between the sides of the board and the points of the board
    if player_color == BLACK:
        #north
        for p in range(BOARD_X):
            if board[p] == player_color or board[p] == EMPTY:
                vcs[p].append(VC(False, "N", p, set()))
                vcs["N"].append(VC(False, p, "N", set()))
        #south
        for p in range(BOARD_SIZE-BOARD_X, BOARD_SIZE):
            if board[p] == player_color or board[p] == EMPTY:
                vcs[p].append(VC(False, "S", p, set()))
                vcs["S"].append(VC(False, p, "S", set()))

    else:
        #west
        for p in range(0, BOARD_SIZE, BOARD_X):
            if board[p] == player_color or board[p] == EMPTY:
                vcs[p].append(VC(False, "W", p, set()))
                vcs["W"].append(VC(False, p, "W", set()))
        #east
        for p in range(BOARD_X-1, BOARD_SIZE, BOARD_X):
            if board[p] == player_color or board[p] == EMPTY:
                vcs[p].append(VC(False, "E", p, set()))
                vcs["E"].append(VC(False, p, "E", set()))

    return vcs

#create a unique hash for a vc
def vc_hash(semi, org, dest, carrier):
    return str(semi) + str(org) + str(dest) + str(carrier)

def or_rule(vcs, board, hashes, shared_color, create_semis):
    new_vcs = []
    #iterate over all destination points
    for p in vcs:
        #only consider shared destinations of the specified color
        if type(p) == str or board[p] != shared_color:
            continue
        for a in vcs[p]:
            #only consider full vcs
            if a.semi:
                continue
            for b in vcs[p]:
                #make sure both vcs have a different origin
                if b.semi or b.org == a.org:
                    continue
                #Create the new carrier as the union of existsing carriers and the shared destination
                new_carrier = a.carrier.union(b.carrier)
                new_carrier.add(p)
                #Make sure the vc hasn't already been created
                if vc_hash(create_semis, a.org, b.org, new_carrier) in hashes:
                    continue
                #Make sure there isn't an existing full vc connecting the same points as the new semi vc
                #and make sure there isn't an existing vc with a subset of the new carrier
                invalid = False
                for c in vcs[b.org]:
                    if c.org == a.org and (not c.semi and (create_semis or c.carrier.issubset(new_carrier))):
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

def and_rule(vcs, board, hashes, empty_points):
    new_vcs = []
    #iterate over all destination points
    for p in vcs:
        for a in vcs[p]:
            #only consider semi vcs
            if not a.semi:
                continue
            for b in vcs[p]:
                #make sure both vcs have a different origin and non-overlapping carriers (only empty points matter)
                if not b.semi or a.org != b.org or empty_points.intersection(a.carrier.intersection(b.carrier)):
                    continue
                #create the new carrier as the union of the existing carriers
                new_carrier = a.carrier.union(b.carrier)
                #make sure the vc hasn't already been created
                if vc_hash(False, a.org, a.dest, new_carrier) in hashes:
                    continue
                #make sure there isn't an existing full vc which uses a subset of the new carrier
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

def remove_redundant_vcs(vcs):
    for p in vcs:
        to_remove = []
        for a in vcs[p]:
            for b in vcs[p]:
                if a != b and a.org == b.org and ((a.semi and not b.semi) or (a.semi == b.semi and b.carrier.issubset(a.carrier))):
                    to_remove.append(a)
                    break
        for vc in to_remove:
            vcs[p].remove(vc)

def h_search(player_color, board):
    print("Board points:")
    print_labeled_board()

    start_time = time.time()
    #Create empty points set
    empty_points = set()
    for i in range(BOARD_SIZE):
        if board[i] == EMPTY:
            empty_points.add(i)
    #Create initial connections
    connections = add_initial_vcs(player_color, board)
    #Iterate the or and and rules until no new vcs are found
    any_changes = True
    vc_hashes = set()
    while any_changes:
        #Standard or rule, create semi connections
        any_changes = or_rule(connections, board, vc_hashes, EMPTY, True) 
        #Or rule except shared destination point is a player stone, create full connections
        any_changes = or_rule(connections, board, vc_hashes, player_color, False) or any_changes
        #And rule, create full connections
        any_changes = and_rule(connections, board, vc_hashes, empty_points) or any_changes
        #Remove any connections which are supersets of other equivalent connections, or are semi connections for fully connected points
        remove_redundant_vcs(connections)

    end_time = time.time()

    #print found vcs
    for p in connections:
        print("\nDestination point:", p)
        for vc in connections[p]:
            vc.print()

    print("\nTime taken:", end_time - start_time)

#init board
hex_board = [0 for i in range(BOARD_SIZE)]
#You can set stones by point index here for example:
hex_board[6] = BLACK
#hex_board[1] = WHITE

#perform h_search
h_search(BLACK, hex_board)
