# simple hex player RBH 2016
import numpy as np
import tttio

class Cell:  e,x,o = 0,1,2
ttt_max_hash = 3**9-1 

Syms = (  # index lists of 8 symmetric permutations of ttt board
((0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)),
((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)),
((0, 2), (0, 1), (0, 0), (1, 2), (1, 1), (1, 0), (2, 2), (2, 1), (2, 0)),
((2, 0), (1, 0), (0, 0), (2, 1), (1, 1), (0, 1), (2, 2), (1, 2), (0, 2)),
((2, 2), (2, 1), (2, 0), (1, 2), (1, 1), (1, 0), (0, 2), (0, 1), (0, 0)),
((2, 2), (1, 2), (0, 2), (2, 1), (1, 1), (0, 1), (2, 0), (1, 0), (0, 0)),
((2, 0), (2, 1), (2, 2), (1, 0), (1, 1), (1, 2), (0, 0), (0, 1), (0, 2)),
((0, 2), (1, 2), (2, 2), (0, 1), (1, 1), (2, 1), (0, 0), (1, 0), (2, 0)))

Win_lines = [ # index lists of 8 winning lines
[(0, 0), (0, 1), (0, 2)] ,
[(0, 0), (1, 0), (2, 0)] ,
[(1, 0), (1, 1), (1, 2)] ,
[(0, 1), (1, 1), (2, 1)] ,
[(2, 0), (2, 1), (2, 2)] ,
[(0, 2), (1, 2), (2, 2)] ,
[(0, 0), (1, 1), (2, 2)] ,
[(0, 2), (1, 1), (2, 0)] ]


class Position:
#  a ttt board with pieces
#  ..X
#  O..
#  ...

  def moves(self):
    L = []
    for j in range(len(self.brd)):
      for k in range(len(self.brd[j])):
        if self.brd[j][k]==Cell.e: 
          L.append((j,k))
    return L

  
  def win_check(self, z):
    win_found = False
    for t in Win_lines:
      if (self.brd[t[0][0]][t[0][1]] == z and
          self.brd[t[1][0]][t[1][1]] == z and
          self.brd[t[2][0]][t[2][1]] == z):
        return True
    return False

  def gameover(self):
    win_found = False
    for z in (Cell.x, Cell.o):
      if (self.win_check(z)):
        print('\n  gameover: ',tttio.cell_to_char(z),'wins\n')
        return True
    return False

  def putstone(self, row, col, color):
    self.brd[row][col] = color

  # usual hash function
  # position 2 1 2 0 0 ... hashes to 2*3^0 + 1*3^1 + 2*3^2 ...
  # return min hash in set of 8 symmetric positions
  def hash(self):
    best = ttt_max_hash + 1 # equivalent to plus infinity
    for j in range(len(Syms)):
      ttl, multiplier = 0, 1
      for tpl in Syms[j]:
        ttl += multiplier * self.brd[tpl[0]][tpl[1]]
        multiplier *=3
      best = min(best,ttl)
      #print('ttl',ttl,best)
    return best

  def __init__(self, rows, cols):
    self.r, self.c =  rows, cols
    self.bsize = rows*cols
    self.brd = np.array(  # to start, all empty
      [[Cell.e]*cols] *rows,\
         dtype = np.int8)
    # non-empty values
    for j in range(self.brd.shape[0]):
      for k in range(self.brd.shape[1]):
        self.brd[j][k] = Cell.e

  def genmove(self, request):
    if request[0]:
      print(' genmove coming soon')
    else:
      print(request[2])

  def makemove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if (tttio.char_to_cell(ch) == Cell.e or 
          tttio.char_to_cell(ch) == Cell.x or 
          tttio.char_to_cell(ch) == Cell.o):
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < self.r and y>=0 and y < 1+self.c:
            self.putstone(x, y, tttio.char_to_cell(ch))
            return
          else: print('\n  coordinate off board')
    print('  ... ? ... sorry ...\n')

def playgame():
  def resize(p, t):
    if t[0]: p = Position(t[1],t[2])
    else:    print(t[3])
    return   p

  p = Position(3,3)
  while True:
    tttio.showboard(p)
    print(p.moves())
    if p.gameover():
      return
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      tttio.printmenu()
    elif cmd[0][0]=='g':
      p.genmove(tttio.genmoverequest(cmd))
    elif cmd[0][0]=='z':
      p = resize(p, tttio.boardsizerequest(cmd))
    elif (cmd[0][0] in tttio.Cell_chars):
        p.makemove(cmd)
    else:
      print('\n try again \n')

playgame()
