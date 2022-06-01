import numpy as np

class Board:
  Empty,Black,White = 0,1,2
  def __init__(self,n):
    self.board = np.zeros((n,n), dtype=int)
    self.size = n

  def show(self):
    print('')
    for j in range(self.size):
      outstr = '  '*j
      for k in range(self.size):
        outstr += str.format('{0:2}'.format(self.board[j,k])) + '  '
      print(outstr)

  def addstone(self,col,r,c):
    self.board[r,c] = col

brd = Board(3)
brd.show()
for j in range(brd.size):
  brd.addstone(1,j,j)
brd.show()
for j in range(brd.size):
  brd.addstone(2,j,j)
brd.show()
      
