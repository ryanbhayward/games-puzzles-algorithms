# 15-Puzzle Solver
# Yoni Elhanani 2019
#    RBH: added node count printing

from typing import List, Iterator, Tuple
from argparse import ArgumentParser
from collections import deque
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


def genNeighbors() -> List[List[int]]:
    "Neighbors of a particular position"
    neighbors: List[List[int]] = [[] for i in range(16)]
    for i in range(4):
        for j in range(3):
            neighbors[4*i+j].append(4*i+j+1)
            neighbors[4*i+j+1].append(4*i+j)
            neighbors[i+4*j].append(i+4*j+4)
            neighbors[i+4*j+4].append(i+4*j)
    return neighbors


neighbors = genNeighbors()


class Node:
    "Nodes record a state and the path to that state"
    def __init__(self, value: State, zero: int, parent: State, move: int) -> None:
        self.value = value      # The state of the node
        self.zero = zero        # The location of the empty place
        self.parent = parent    # The state of the parent node
        self.move = move        # The stone that moved

    def children(self) -> Iterator["Node"]:
        "Generates subnodes for the given node"
        for location in neighbors[self.zero]:
            # Negative values stand for fixed stones
            if self.value[location] > 0:
                next = nextState(self.value, location, self.zero)
                yield Node(next, location, self.value, self.zero)


def BFS(state: State, fixed: List[int], goal: List[int], verbose: bool) -> Tuple[List[int], int]:
    "Performs BFS search without moving the fixed stones, until all goal stones are in place"
    # Negative values are fixed stones.
    # There are stones for which we are indifferent to their location at a particular stage.
    # By not distinguishing them, we significantly reduce the state space for this problem.
    # For convinience, they are all given the value 16.
    source = tuple(-1 if x in fixed else 16 if x not in [0] + goal else x for x in state)
    if all(source[(n-1) % 16] == n for n in goal):
        return ([], 0)
    zero = source.index(0)
    DAG = {source: Node(source, zero, source, zero)}
    queue = deque(DAG[source].children())
    iterations = 0
    while queue:
        iterations += 1
        # if 0 == iterations % 1000: print(iterations, "iterations")
        node = queue.pop()
        if node.value not in DAG:
            DAG[node.value] = node
            queue.extendleft(node.children())
            if all(node.value[(n-1) % 16] == n for n in goal):
                path = [node.zero, node.move]
                while node.value != source:
                    path.append(node.move)
                    node = DAG[node.parent]
                if verbose:
                    print("nodes searched", iterations)
                return (path[-2::-1], iterations)
    raise Exception("Odd Permutation. Impossible to reach destination")


def solve15(state: State, stages: List[List[int]], verbose: bool) -> Tuple[int, int]:
    "Solves the puzzle in stages"
    # At each stage we find the shortest path to reach the next stage.
    # Then we apply it to the current state and continue to the next stage from there.
    if verbose:
        print(showState(state))
    zero = state.index(0)
    fixed = []
    movecount = 0
    stagecount = 0
    iterations = 0
    for goal in stages:
        stagecount += 1
        if verbose:
            print(f"\nStage {stagecount}:\n")
        path, subiter = BFS(state, fixed, goal, verbose)
        iterations += subiter
        for x in path:
            if zero != x:
                movecount += 1
                state = nextState(state, zero, x)
                zero = x
                if verbose:
                    print(showState(state))
                    print(f"Moves: {movecount}")
        fixed += goal
    if verbose:
        print()
        print(f"Total nodes searched: {iterations}")
    return (movecount, iterations)


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
    parser.add_argument('--perm', '-p', metavar='i', type=int, nargs='+',
                        help='A permutation of 1..15')
    parser.add_argument('--staging', '-s', metavar='n', action='store', type=int, default=1,
                        help='Staging schedule')
    parser.add_argument('--batch', '-b', metavar='n', action='store', type=int, default=0,
                        help='Batch statistics')
    args = parser.parse_args()
    optlevels = [[[1, 2], [3, 4], [5, 6], [7, 8], [9, 13], [10, 14], [11, 12, 15]],
                 [[1, 2], [3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]],
                 [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]]]
    assert 0 < args.staging <= len(optlevels), "Staging schedule does not exist"
    if args.batch:
        print("moves\tnodes")
        for _ in range(args.batch):
            input = even_random(10000)
            moves, nodes = solve15(tuple(input) + (0, ), optlevels[args.staging-1], False)
            print(f"{moves}\t{nodes}")
    else:
        if not args.perm:
            input = even_random(10000)
        else:
            input = args.perm
            assert sorted(input) == list(range(1, 16)), "Invalid permutation"
        solve15(tuple(input) + (0, ), optlevels[args.staging-1], True)
