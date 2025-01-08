from Go import GoGame
from Hex import HexGame
import random

VERBOSE = False
PRINT_ITERATIONS = True
ITER_FREQ = 100
WR_WEIGHT = 1

class Node:
    def __init__(self, move):
        self.children = []
        self.move = move
        self.expanded = False
        self.wins = 1
        self.visits = 2
        self.ewLoss = 0
        self.ewWin = 0

    def RemoveChild(self, move):
        for i in range(len(self.children)):
            if self.children[i].move == move:
                del self.children[i]
                return

    def Value(self, pVisits):
        return (WR_WEIGHT / (WR_WEIGHT + pVisits)) * (self.ewLoss / (1 - self.wins / self.visits))\
            + (1 - (WR_WEIGHT / (WR_WEIGHT + pVisits))) * (1 / (1 - self.wins / self.visits))

    def SortChildren(self):
        if len(self.children) <= 1:
            return
        self.children.sort(key=lambda x: x.Value(self.visits))

    def UpdateWinRate(self, wins, visits):
        self.wins += wins
        self.visits += visits

    def UpdateEW(self):
        self.ewLoss = sum([child.ewWin for child in self.children])
        self.ewWin = 0
        p = 1
        for child in self.children:
            self.ewWin += p * child.ewLoss
            p *= child.wins / child.visits

    def PrintChildren(self):
        print("[", end="")
        for c in self.children:
            print(c.move, end=", ")
        print("]")

class EWS:
    def __init__(self, game):
        self.game = game

    def Evaluate(self, node):
        if VERBOSE:
            print("Evaluate")
            self.game.Print()
        toPlay = True
        numMoves = 0
        node.visits += 1
        self.game.takeSnapshot()
        while True:
            moves = self.game.GetMoves()
            if VERBOSE:
                print(moves)
            node.ewLoss += len(moves)
            node.ewWin += len(moves)
            move = moves[random.randint(0, len(moves) - 1)]
            self.game.MakeMove(move, False)
            if VERBOSE:
                print(move)
                self.game.Print()
            numMoves += 1
            isTerminal, isWinning = self.game.IsTerminal()
            if isTerminal:
                if isWinning == toPlay:
                    node.wins += 1
                    self.game.restoreSnapshot()
                    if VERBOSE:
                        print("win")
                    return True
                else:
                    self.game.restoreSnapshot()
                    if VERBOSE:
                        print("loss")
                    return False
            toPlay = not toPlay


    def Expand(self, node):
        if VERBOSE:
            print("Expand")
            self.game.Print()
        node.expanded = True
        wins = 0
        visits = 0
        for m in self.game.GetMoves():
            self.game.MakeMove(m)
            isTerminal, isWinning = self.game.IsTerminal() # isWinning is for the last player to move
            if VERBOSE:
                print("move", m, "terminal", isTerminal, "winning", isWinning)
            if isTerminal and isWinning:
                if VERBOSE:
                    print("Winning child:", m)
                    self.game.Print()
                    print()
                self.game.UndoMove()
                return True, True, 1, 1
            elif not isTerminal:
                child = Node(m)
                node.children.append(child)
                childWon = self.Evaluate(child)
                if not childWon:
                    wins += 1
                visits += 1
            self.game.UndoMove()

        if VERBOSE:
            node.PrintChildren()
            print()
        return len(node.children) == 0, False, wins, visits

    def SelectBackpropagate(self, node):
        child = node.children[0]
        childMove = child.move
        if VERBOSE:
            print("SB")
            self.game.Print()
            node.PrintChildren()
            print("MOVE", childMove)
            print()
        self.game.MakeMove(childMove)
        if child.expanded:
            isSolved, isWinning, wins, visits = self.SelectBackpropagate(child)
        else:
            isSolved, isWinning, wins, visits = self.Expand(child)
        self.game.UndoMove()
        if VERBOSE:
            print("UNDO")
            self.game.Print()
        wins = visits - wins
        node.UpdateWinRate(wins, visits)

        if isSolved and isWinning:
            node.RemoveChild(childMove)
            if VERBOSE:
                print("Solved child")
                node.PrintChildren()
            if len(node.children) == 0:
                if VERBOSE:
                    print("Solved losing")
                return True, False, wins, visits
        elif isSolved and not isWinning:
            if VERBOSE:
                print("Solved winning")
            return True, True, wins, visits

        node.SortChildren()
        node.UpdateEW()
        if VERBOSE:
            print("Unsolved")
            node.PrintChildren()
            print()
        return False, False, wins, visits


    def Solve(self):
        random.seed()
        self.game.Reset()
        self.game.Print()
        root = Node(None)
        self.Expand(root)
        isSolved, isWinning, _, _ = self.SelectBackpropagate(root)
        iteration = 0
        while not isSolved:
            if VERBOSE:
                print("------------------------------------------")
            if PRINT_ITERATIONS and iteration % ITER_FREQ == 0:
                print("Iteration num:", iteration)
                print("Root child nodes:")
                print("Move coords, win rate, visits, ewLoss, ewWin")
                for child in root.children:
                    print(child.move, round(child.wins / child.visits, 3), child.visits, round(child.ewLoss), round(child.ewWin))
                print()
                c = root
                print("Branching factors of last line searched:")
                while len(c.children) > 0:
                    print(len(c.children), end=" ")
                    c = c.children[0]
                print()
                print()
                
            iteration += 1
            if VERBOSE:
                input("Press enter to continue...")
            isSolved, isWinning, _, _ = self.SelectBackpropagate(root)
        print(iteration)
        return isWinning

# Accept user commands
def GTP_loop():
    ews = EWS(HexGame(3, 3, 0.5))
    print("Known commands:")
    print("quit")
    print("boardsize")
    print("komi")
    print("play")
    print("undo")
    print("showboard")
    print("solve")
    print("game {hex, go}")
    while True:
        # Parse entered command
        entered = input()
        if len(entered) == 0:
            continue
        if " " in entered:
            cmd, argstr = entered.split(" ", 1)
            args = argstr.split(" ")
        else:
            cmd = entered
            args = []

        if cmd == "quit":
            break
        elif cmd == "list_commands" or cmd == "help" or cmd == "-h":
            print("quit")
            print("boardsize")
            print("komi")
            print("play")
            print("undo")
            print("showboard")
            print("solve")
        elif cmd == "boardsize":
            if len(args) == 1:
                try:
                    size = int(args[0])
                    if size < 1 or size > 19:
                        print("? size out of range")
                    else:
                        ews.game.ResetXY(size, size)
                        print("= ")
                except ValueError:
                    print("? size not an integer")
            else:
                print("? boardsize requires 1 argument")
        elif cmd == "komi":
            if len(args) == 1:
                try:
                    komi = float(args[0])
                    ews.game.komi = komi
                    print("= ")
                except ValueError:
                    print("? komi not a number")
            else:
                print("? komi requires 1 argument")
        elif cmd == "play":
            if len(args) == 2:
                try:
                    x = int(args[0])
                    y = int(args[1])
                    if x < 0 or x >= ews.game.xSize or y < 0 or y >= ews.game.ySize:
                        print("? vertex out of range")
                    else:
                        ews.game.MakeMove((x, y))
                        ews.game.Print()
                        print(ews.game.GetMoves())
                        print("= ")
                except ValueError:
                    print("? vertex not an integer")
            elif len(args) == 1:
                    if args[0] == "pass" or args[0] == "None":
                        ews.game.MakeMove(None)
                        ews.game.Print()
                        print("= ")
                    else:
                        print("? invalid vertex")
            else:  
                print("? play requires 1 or 2 arguments")
        elif cmd == "undo":
            ews.game.UndoMove()
            print("= ")
        elif cmd == "showboard":
            ews.game.Print()
            print("= ")
        elif cmd == "solve":
            print("= " + str(ews.Solve()))
        elif cmd == "game":
            if len(args) == 1:
                if args[0] == "hex":
                    ews.game = HexGame(3, 3, 0.5)
                    print("= ")
                elif args[0] == "go":
                    ews.game = GoGame(3, 3, 8.5)
                    print("= ")
                else:
                    print("? unknown game")
            else:
                print("? game requires 1 argument")
        else:
            print("? unknown command")

if __name__ == "__main__":
    GTP_loop()