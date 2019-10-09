# 15-Puzzle Solver
# Yoni Elhanani 2019

from typing import List, Iterator, Tuple
from argparse import ArgumentParser
from heapq import heappop, heappush
from random import randrange


# A state is a configuration of stones on the board
State = Tuple[int, ...]


def showState(state: State) -> str:
    "Prints the state of the board"
    divider = "\n|" + "----+" * 3 + "----|\n"
    output = divider
    for i in range(4):
        output += "|"
        for j in range(4):
            n = state[4*i+j]
            output += " " + str(n) if n else "  "
            if n < 10:
                output += " "
            output += " |"
        output += divider
    return output


def nextState(source: State, pos1: int, pos2: int) -> State:
    "Next state of the board, after switching 2 stones"
    L = list(source)
    L[pos1], L[pos2] = L[pos2], L[pos1]
    return tuple(L)


def genNeignbors() -> List[List[int]]:
    "Neighbors of a particular position"
    neighbors: List[List[int]] = [[] for i in range(16)]
    for i in range(4):
        for j in range(3):
            neighbors[4*i+j].append(4*i+j+1)
            neighbors[4*i+j+1].append(4*i+j)
            neighbors[i+4*j].append(i+4*j+4)
            neighbors[i+4*j+4].append(i+4*j)
    return neighbors


neighbors = genNeignbors()


def tile_distance(i: int, n: int) -> int:
    "Finds the l1 distance between 2 tiles"
    if n > 0:
        srccol, srcrow = divmod(n-1, 4)
        dstcol, dstrow = divmod(i, 4)
        return abs(srccol-dstcol) + abs(srcrow-dstrow)
    else:
        return 0


def state_distance(state: State) -> int:
    "Computes the l1 norm of a particular state"
    return sum(tile_distance(i, n) for i, n in enumerate(state))


# @total_ordering
class Node:
    "Nodes record a state, the path to that state, and distances"

    # Optimization > 1 is BFS
    # Optimization = 1/k is a k-approximation (gurantees at most k times more than shortest path)
    # Optimization = 1 is shortest path
    # Optimization = 0 is the quickest solver (indifferent to path length).
    # Optimization < -1 is DFS
    opt = 0

    def __init__(self, value: State, zero: int, parent: State, move: int,
                 dstdist: int, srcdist: int) -> None:
        self.value = value        # The state of the node
        self.zero = zero          # The location of the empty place
        self.parent = parent      # The state of the parent node
        self.move = move          # The stone that moved
        self.dstdist = dstdist    # The l1-distance to the terminal node
        self.srcdist = srcdist    # The moves count from the source terminal node

    def children(self) -> Iterator["Node"]:
        "Generates subnodes for the given node"
        for location in neighbors[self.zero]:
            face = self.value[location]
            next = nextState(self.value, location, self.zero)
            diff = tile_distance(self.zero, face) - tile_distance(location, face)
            yield Node(next, location, self.value, self.zero,
                       self.dstdist + diff, self.srcdist + 1)

    def __lt__(self, other):
        return self.dstdist + Node.opt*self.srcdist < other.dstdist + Node.opt*other.srcdist


def AStar(state: State) -> List[State]:
    "Performs A* search to find shortest path to terminal state"
    source = state
    zero = source.index(0)
    distance = state_distance(state)
    DAG = {}
    heap = [Node(source, zero, source, zero, distance, 0)]
    while heap:
        node = heappop(heap)
        if node.value not in DAG:
            DAG[node.value] = node
            path = []
            if node.dstdist == 0:
                while node.value != node.parent:
                    path.append(node.value)
                    node = DAG[node.parent]
                return path[::-1]
            for child in node.children():
                heappush(heap, child)
    raise Exception("Odd Permutation. Impossible to reach destination")


def solve15(state: State, opt: float) -> None:
    "Solves the puzzle"
    Node.opt = opt
    idx = 0
    print(f"Move: {idx}, Distance: {state_distance(state)}")
    print(showState(state))
    for p in AStar(state):
        idx += 1
        print(f"Move: {idx}, Distance: {state_distance(p)}")
        print(showState(p))


def even_random(n: int) -> List[int]:
    "Generates a random even permutation"
    # A permutation is even iff it can be written as a product of 3-cycles.
    L = list(range(1, 16))
    for _ in range(n):
        a = randrange(15)
        b = randrange(15)
        c = randrange(15)
        if a != b and b != c and a != c:
            L[a], L[b], L[c] = L[b], L[c], L[a]
    return L


if __name__ == "__main__":
    parser = ArgumentParser(description='15-puzzle solver')
    parser.add_argument('--perm', '-p', metavar="i", type=int, nargs='+',
                        help='A permutation of 1..15')
    parser.add_argument('--opt', '-o', metavar="n", action='store', type=float, default=50,
                        help='Optimization percent')
    args = parser.parse_args()
    if not args.perm:
        input = even_random(10000)
    else:
        input = args.perm
        assert sorted(input) == list(range(1, 16)), "Invalid permutation"
    solve15(tuple(input) + (0, ), min(args.opt/100, 1))
