# linear go
import sys
from paint_chars import paint
# add move history
# add scoring

class LGoBoard:
  def __init__(self,numcells):
    self.Black, self.White, self.Empty, self.Edge = range(4)
    self.stone = '*o-%'  # black white empty edge
    self.n = numcells
    # board as string
    self.b =  self.stone[self.Edge]\
            + self.stone[self.Empty] * numcells + self.stone[self.Edge]
    # for locations of cells that are left-end or right-end of a group,
    #   the number of cells in that group
    self.size = [1] * (numcells+2)

  def eraseStones(self,psn,k):
    self.b = self.b[:psn]+self.stone[self.Empty]*k+ self.b[psn+k:]
    for j in range(psn,psn+k): self.size[j] =1

  def addCell(self,psn,color):
    self.b = self.b[:psn] + self.stone[color] + self.b[psn+1:]
    if self.b[psn] == self.b[psn-1]: # matches stone to its left
      if self.b[psn] == self.b[psn+1]: # matches stone to its right
        newsize = 1 + self.size[psn-1] + self.size[psn+1]
        self.size[psn-self.size[psn-1]] = newsize #update on left end
        self.size[psn+self.size[psn+1]] = newsize #update on right end
      else: # matches on left but not right
        newsize = 1 + self.size[psn-1] 
        self.size[psn-self.size[psn-1]] = newsize #update on left end
        self.size[psn] = newsize                  #update on right end
    elif self.b[psn] == self.b[psn+1]: # matches right but not left
      newsize = 1 + self.size[psn+1] 
      self.size[psn] = newsize                    #update on left end
      self.size[psn+self.size[psn+1]] = newsize   #update on right end

  def isEmpty(self,psn):
    return self.b[psn] == self.stone[self.Empty]

  def leftGroupStrong(self,psn): # group to left has extra liberty ?
    assert(self.isEmpty(psn) and not self.isEmpty(psn-1))
    return self.isEmpty(psn-self.size[psn-1])

  def rightGroupStrong(self,psn): # group to right has extra liberty ?
    assert(self.isEmpty(psn) and not self.isEmpty(psn+1))
    return self.isEmpty(psn+self.size[psn+1])

  def leftCapture(self, psn, color): # move will capture left group ?
    return (self.b[psn-1] == self.stone[1-color] and
       not self.isEmpty(psn-(1+self.size[psn-1])))

  def rightCapture(self, psn, color): # move will capture right group ?
    return (self.b[psn+1] == self.stone[1-color] and
       not self.isEmpty(psn+(1+self.size[psn+1])))
  
  def isLegalMove(self, psn, color):
    return self.isEmpty(psn) and (
      self.isEmpty(psn-1) or self.isEmpty(psn+1) or
      (self.b[psn-1] == self.stone[color] and
       self.isEmpty(psn-(1+self.size[psn-1]))) or
      (self.b[psn+1] == self.stone[color] and
       self.isEmpty(psn+1+self.size[psn+1])) or
       self.leftCapture(psn,color) or
       self.rightCapture(psn,color) )

  def makeLegalMove(self, psn, color):
    assert self.isLegalMove(psn,color)
    if self.leftCapture(psn,color): 
      self.eraseStones(psn-self.size[psn-1],self.size[psn-1])
    if self.rightCapture(psn,color): 
      self.eraseStones(psn+1,self.size[psn+1])
    self.addCell(psn,color)

  def show(self):    
    sizestr = ''   # print group sizes
    for j in range(2+self.n):
      if self.size[j] < 10: sizestr += ' '
      sizestr += ' ' + str(self.size[j])

    indexstr = '   '   # print cell indices 
    for j in range(self.n):
      if j+1 < 10: indexstr += ' '
      indexstr += ' ' + str(j+1)

    cellstr = ''    # then print cell contents
    for c in self.b:  
      cellstr += '  ' + c
    print(paint(indexstr + '\n' + cellstr + '\n' + sizestr, self.stone))

    for ptm in range(2):
      print('\nlegal ' + self.stone[ptm] + ' ', end='')
      for j in range(2+self.n):
        if self.isLegalMove(j,ptm): print(j, end='')
    print('')
    print('score [black white]: ', self.score())

  def score(self): # black territory - white territory
    territory = [0,0]
    j, last_non_empty = 1, 0 # psn on board, psn of left edge
    while j < 1 + self.n:
      color = self.stone.index(self.b[j])
      if color < 2:  # black or white
        if last_non_empty < j-1 and (
             last_non_empty == 0 or  # left edge
             color == last_color):
          territory[color] += j - last_non_empty
        else:
          territory[color] += 1
        last_non_empty, last_color = j, color
      j += 1
    if last_non_empty > 0 and last_non_empty < j-1:
      color = self.stone.index(self.b[last_non_empty])
      territory[color] += (j-1) - last_non_empty
    return territory

#def showHistory(h):
  #for j in range(len(h)):
    #print j, 
    #showBoard(h[j])

def getCommand(color):
  print('\n ' + color + '  cell ', end='')
  line = sys.stdin.readline()
  print('')
  if line[0] == '\n': 
    return -2 # end game
  elif not line.split()[0].isdigit(): 
    return -1 # bad input, retry
  else: 
    return int(line.split()[0])

def playGame(board):
  ptm = board.Black # player to move: 1st player
  while True:
    board.show()
    m = getCommand(board.stone[ptm])
    if   m == -2: break
    elif m == -1: print('sorry ? ... ')
    elif m ==  0: 
      print('pass\n')
      ptm = 1 - ptm
    elif m > board.n: print('out of bounds')
    elif not board.isLegalMove(m,ptm): 
      print(' illegal ... try again\n')
    else: 
      board.makeLegalMove(m,ptm)
      ptm = 1 - ptm
  print('  adios ... sayonara ... annyeong ... zaijian ...\n')

brd = LGoBoard(8)
playGame(brd)
