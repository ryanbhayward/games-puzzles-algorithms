import copy

VERBOSE = False

EMPTY = 0
BLACK = 1
WHITE = 2
PASS = None

class GoGame:

    def __init__(self, xSize, ySize, komi):
        self.komi = komi
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
        self.passHistory = []

    def Print(self):
        for y in range(self.ySize):
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
        self.numPassesCopy = self.numPasses

    def restoreSnapshot(self):
        self.board = self.boardCopy
        self.colorToPlay = self.colorToPlayCopy
        self.numPasses = self.numPassesCopy

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
        if y < self.ySize - 1:
            adj.append((x, y + 1))

    def AdjPointsC(self, point, color):
        x, y = point
        adj = []
        if x > 0 and self.board[x - 1][y] == color:
            adj.append((x - 1, y))
        if x < self.xSize - 1 and self.board[x + 1][y] == color:
            adj.append((x + 1, y))
        if y > 0 and self.board[x][y - 1] == color:
            adj.append((x, y - 1))
        if y < self.ySize - 1 and self.board[x][y + 1] == color:
            adj.append((x, y + 1))
        return adj

    def IsAdjTo(self, point, color):
        x, y = point
        if x > 0 and self.board[x - 1][y] == color:
            return True
        if x < self.xSize - 1 and self.board[x + 1][y] == color:
            return True
        if y > 0 and self.board[x][y - 1] == color:
            return True
        if y < self.ySize - 1 and self.board[x][y + 1] == color:
            return True
        return False

    def HasLiberty(self, point):
        x, y = point
        color = self.board[x][y]
        toCheck = [point]
        checked = set()
        while len(toCheck) > 0:
            curr = toCheck.pop()
            checked.add(curr)
            if self.IsAdjTo(curr, EMPTY):
                return True
            adjC = self.AdjPointsC(curr, color)
            for point in adjC:
                if point not in checked and point not in toCheck:
                    toCheck.append(point)
        return False

    def IsLegalMove(self, move):
        if move == PASS:
            return True
        x, y = move
        if self.board[x][y] != EMPTY:
            return False
        self.MakeMove(move)
        ko = False
        for b in self.history:
            ko = True
            for x in range(self.xSize):
                for y in range(self.ySize):
                    if b[x][y] != self.board[x][y]:
                        ko = False
                        break
                if not ko:
                    break
            if ko:
                break
        if ko:
            self.UndoMove()
            return False

        if not self.HasLiberty(move):
            self.UndoMove()
            return False

        self.UndoMove()
        return True

    def GetMoves(self):
        moves = [PASS]
        for x in range(self.xSize):
            for y in range(self.ySize):
                if self.IsLegalMove((x, y)):
                    moves.append((x, y))
        return moves

    def RemoveBlock(self, point):
        x, y = point
        color = self.board[x][y]
        toCheck = [point]
        checked = set()
        while len(toCheck) > 0:
            curr = toCheck.pop()
            checked.add(curr)
            self.board[curr[0]][curr[1]] = EMPTY
            adjC = self.AdjPointsC(curr, color)
            for point in adjC:
                if point not in checked and point not in toCheck:
                    toCheck.append(point)

    def MakeMove(self, move, storeHistory=True):
        if storeHistory:
            self.history.append(copy.deepcopy(self.board))
            self.passHistory.append(self.numPasses)

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

        if move == PASS:
            self.numPasses += 1
            self.colorToPlay = self.GetOpponent(self.colorToPlay)
            return
        
        self.numPasses = 0
        x, y = move
        self.board[x][y] = self.colorToPlay
        adjOpp = self.AdjPointsC(move, self.GetOpponent(self.colorToPlay))
        for point in adjOpp:
            if not self.HasLiberty(point):
                self.RemoveBlock(point)

        self.colorToPlay = self.GetOpponent(self.colorToPlay)
    
    def UndoMove(self):
        self.board = self.history.pop()
        self.colorToPlay = self.GetOpponent(self.colorToPlay)
        self.numPasses = self.passHistory.pop()

    def IsTerminal(self):
        if self.numPasses >= 2:
            checked = set()
            blackScore = 0
            whiteScore = 0
            for x in range(self.xSize):
                for y in range(self.ySize):
                    if (x, y) not in checked:
                        checked.add((x, y))
                        if self.board[x][y] == BLACK:
                            blackScore += 1
                        elif self.board[x][y] == WHITE:
                            whiteScore += 1
                        else:
                            toCheck = [(x, y)]
                            blackAdj = False
                            whiteAdj = False
                            numPoints = 0
                            while len(toCheck) > 0:
                                curr = toCheck.pop()
                                checked.add(curr)
                                numPoints += 1
                                if self.IsAdjTo(curr, BLACK):
                                    blackAdj = True
                                if self.IsAdjTo(curr, WHITE):
                                    whiteAdj = True
                                adj = self.AdjPointsC(curr, EMPTY)
                                for point in adj:
                                    if point not in checked and point not in toCheck:
                                        toCheck.append(point)
                            if blackAdj and not whiteAdj:
                                blackScore += numPoints
                            elif whiteAdj and not blackAdj:
                                whiteScore += numPoints
            if blackScore > whiteScore + self.komi:
                return True, self.colorToPlay == WHITE
            else:
                return True, self.colorToPlay == BLACK

        return False, False

    