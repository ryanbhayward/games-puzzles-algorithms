# 15-Puzzle Solver
# Yoni Elhanani 2019

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


def BFS(state: State, fixed: List[int], goal: List[int]) -> List[int]:
    "Performs BFS search without moving the fixed stones, until all goal stones are in place"
    # Negative values are fixed stones.
    # There are stones for which we are indifferent to their location at a particular stage.
    # By not distinguishing them, we significantly reduce the state space for this problem.
    # For convinience, they are all given the value 16.
    source = tuple(-1 if x in fixed else 16 if x not in [0] + goal else x for x in state)
    if all(source[(n-1) % 16] == n for n in goal):
        return []
    zero = source.index(0)
    DAG = {source: Node(source, zero, source, zero)}
    queue = deque(DAG[source].children())
    while queue:
        node = queue.pop()
        if node.value not in DAG:
            DAG[node.value] = node
            queue.extendleft(node.children())
            if all(node.value[(n-1) % 16] == n for n in goal):
                path = [node.zero, node.move]
                while node.value != source:
                    path.append(node.move)
                    node = DAG[node.parent]
                return path[-2::-1]
    raise Exception("Odd Permutation. Impossible to reach destination")


def solve15(state: State, stages: List[List[int]]) -> None:
    "Solves the puzzle in stages"
    # At each stage we find the shortest path to reach the next stage.
    # Then we apply it to the current state and continue to the next stage from there.
    print(showState(state))
    zero = state.index(0)
    fixed = []
    movecount = 0
    stagecount = 0
    for goal in stages:
        stagecount += 1
        print(f"\nStage {stagecount}:\n")
        for x in BFS(state, fixed, goal):
            if zero != x:
                movecount += 1
                state = nextState(state, zero, x)
                zero = x
                print(f"Moves: {movecount}")
                print(showState(state))
        fixed += goal


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
    args = parser.parse_args()
    if not args.perm:
        input = even_random(10000)
    else:
        input = args.perm
        assert sorted(input) == list(range(1, 16)), "Invalid permutation"
    optlevels = [[[1, 2], [3, 4], [5, 6], [7, 8], [9, 13], [10, 14], [11, 12, 15]],
                 [[1, 2], [3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]],
                 [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12, 13, 14, 15]]]
    assert 0 < args.staging <= len(optlevels), "Staging schedule does not exist"
    solve15(tuple(input) + (0, ), optlevels[args.staging-1])
