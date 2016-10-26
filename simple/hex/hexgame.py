# simple hex player RBH 2016
import numpy as np
import hexio
from hexio import Cell
from wincheck import BFSWinCheck
  
class Hexposition:
#  a hex board with 
#  board encircled with ring(s): top/btm black, sides white
#  --******--
#   --******--
#    oo......oo
#     oo......oo
#      oo......oo
#       oo......oo
#        oo......oo
#         oo......oo
#          --******--
#           --******--
  def gameover(self):
    return False

  def putstone(self, row, col, color):
    self.brd[self.rings + row][self.rings + col] = color

  def __init__(self, rows, cols):
    self.rings = 1
    assert(self.rings > 0)
    self.r, self.c =  rows, cols
    self.bsize = (2*self.rings+rows)*(2*self.rings+cols)
    self.brd = np.array(  # to start, all empty
      [[Cell.e]*(2*self.rings+cols)] *(2*self.rings+rows),\
         dtype = np.int8)
    # non-empty values
    for j in range(self.brd.shape[0]):
      for k in range(self.brd.shape[1]):
        if j < self.rings or j >= rows + self.rings:
          self.brd[j][k] = Cell.b
    for j in range(self.brd.shape[0]):
      for k in range(self.brd.shape[1]):
        if k < self.rings or k >= cols + self.rings:
          if self.brd[j][k] == Cell.b: 
            self.brd[j][k] = Cell.bw
          else:
            self.brd[j][k] = Cell.w

  def genmove(self, request):
    if request[0]:
      print(' genmove coming soon')
    else:
      print(request[2])

  def makemove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if (hexio.char_to_cell(ch) == Cell.b or 
          hexio.char_to_cell(ch) == Cell.w):
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < self.r and y>=0 and y < 1+self.c:
            self.putstone(x, y, hexio.char_to_cell(ch))
            return
          else: print('\n  coordinate off board')
    print('\n  ... try again ...\n')

def playgame():
  def resize(h, t):
    if t[0]: h = Hexposition(t[1],t[2])
    else:    print(t[3])
    return   h

  h = Hexposition(2,3)
  while True:
    hexio.showboard(h)
    if h.gameover():
      print('\n game over ... who won ? \n')
      return
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      hexio.printmenu()
    elif cmd[0][0]=='u':
      print('undo coming soon')
    elif cmd[0][0]=='g':
      h.genmove(hexio.genmoverequest(cmd))
    elif cmd[0][0]=='z':
      h = resize(h, hexio.boardsizerequest(cmd))
    elif (cmd[0][0]== hexio.Cell_chars[Cell.b] or
      cmd[0][0]== hexio.Cell_chars[Cell.w]):
        h.makemove(cmd)
    elif (cmd[0][0]=='w'):
      win_validator = BFSWinCheck(h)
      ch = cmd.split()[1]
      try:
          print(' '+str(win_validator.check(ch)))
      except ValueError:
        print(' not valid input')
    else:
      print('\n try again \n')

playgame()
