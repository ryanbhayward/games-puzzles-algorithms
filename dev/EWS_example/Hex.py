import copy

VERBOSE = False

EMPTY = 0
BLACK = 1
WHITE = 2

class HexGame:

    def __init__(self, xSize, ySize, komi):
        self.ResetXY(xSize, ySize)

    def ResetXY(self, xSize, ySize):
        self.xSize = xSize
        self.ySize = ySize
        self.Reset()

    def Reset(self):
        self.board = [[EMPTY for i in range(self.ySize)] for j in range(self.xSize)]
        self.colorToPlay = BLACK
        self.numPasses = 0
        self.history = []

    def Print(self):
        indent = ""
        for y in range(self.ySize):
            print(indent, end="")
            indent += " "
            for x in range(self.xSize):
                if self.board[x][y] == BLACK:
                    print("B", end=" ")
                elif self.board[x][y] == WHITE:
                    print("W", end=" ")
                else:
                    print(".", end=" ")
            print()

    def takeSnapshot(self):
        self.boardCopy = copy.deepcopy(self.board)
        self.colorToPlayCopy = self.colorToPlay

    def restoreSnapshot(self):
        self.board = self.boardCopy
        self.colorToPlay = self.colorToPlayCopy

    def GetOpponent(self, color):
        if color == BLACK:
            return WHITE
        return BLACK

    def AdjPoints(self, point):
        x, y = point
        adj = []
        if x > 0:
            adj.append((x - 1, y))
        if x < self.xSize - 1:
            adj.append((x + 1, y))
        if y > 0:
            adj.append((x, y - 1))
        if y > 0 and x < self.xSize - 1:
            adj.append((x + 1, y - 1))
        if y < self.ySize - 1:
            adj.append((x, y + 1))
        if y < self.ySize - 1 and x > 0:
            adj.append((x - 1, y + 1))

    def AdjPointsC(self, point, color):
        x, y = point
        adj = []
        if x > 0 and self.board[x - 1][y] == color:
            adj.append((x - 1, y))
        if x < self.xSize - 1 and self.board[x + 1][y] == color:
            adj.append((x + 1, y))
        if y > 0 and self.board[x][y - 1] == color:
            adj.append((x, y - 1))
        if y > 0 and x < self.xSize - 1 and self.board[x + 1][y - 1] == color:
            adj.append((x + 1, y - 1))
        if y < self.ySize - 1 and self.board[x][y + 1] == color:
            adj.append((x, y + 1))
        if y < self.ySize - 1 and x > 0 and self.board[x - 1][y + 1] == color:
            adj.append((x - 1, y + 1))
        return adj

    def IsAdjTo(self, point, color):
        x, y = point
        if x > 0 and self.board[x - 1][y] == color:
            return True
        if x < self.xSize - 1 and self.board[x + 1][y] == color:
            return True
        if y > 0 and self.board[x][y - 1] == color:
            return True
        if y > 0 and x < self.xSize - 1 and self.board[x + 1][y - 1] == color:
            return True
        if y < self.ySize - 1 and self.board[x][y + 1] == color:
            return True
        if y < self.ySize - 1 and x > 0 and self.board[x - 1][y + 1] == color:
            return True
        return False

    def GetMoves(self):
        moves = []
        for x in range(self.xSize):
            for y in range(self.ySize):
                if self.board[x][y] == EMPTY:
                    moves.append((x, y))
        return moves

    def MakeMove(self, move, storeHistory=True):
        if storeHistory:
            self.history.append(copy.deepcopy(self.board))

            if VERBOSE:
                print()
                print("HISTORY:")
                for b in self.history:
                    for y in range(self.ySize):
                        for x in range(self.xSize):
                            if b[x][y] == BLACK:
                                print("B", end=" ")
                            elif b[x][y] == WHITE:
                                print("W", end=" ")
                            else:
                                print(".", end=" ")
                        print()
                    print()
                print()

        x, y = move
        self.board[x][y] = self.colorToPlay
        self.colorToPlay = self.GetOpponent(self.colorToPlay)
    
    def UndoMove(self):
        self.board = self.history.pop()
        self.colorToPlay = self.GetOpponent(self.colorToPlay)

    def IsTerminal(self):
        player = self.GetOpponent(self.colorToPlay)
        checked = set()
        if player == BLACK:
            initPoints = [(i, 0) for i in range(self.xSize)]
        else:
            initPoints = [(0, i) for i in range(self.ySize)]
        for point in initPoints:
            if self.board[point[0]][point[1]] == player and point not in checked:
                toCheck = set([point])
                checked.add(point)
                while len(toCheck) > 0:
                    point = toCheck.pop()
                    if (player == BLACK and point[1] == self.ySize - 1) or (player == WHITE and point[0] == self.xSize - 1):
                        return True, True
                    adj = set(self.AdjPointsC(point, player))
                    for a in adj:
                        if a not in checked:
                            toCheck.add(a)
                            checked.add(a)
        return False, False
