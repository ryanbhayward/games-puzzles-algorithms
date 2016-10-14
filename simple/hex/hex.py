# simple hex player RBH 2016
import numpy as np
from random import shuffle

# global constants
Rings      = 1  # wrapping around the playing board
Cell_chars = '*@-.'

# each cell is empty, black, white, or black-and-white (e.g. dead)
class Cell(): 
  b, w, bw, e  = 0, 1, 2, 3
  
def cell_to_char(n): return Cell_chars[n]
  #if   c==Cell.e:  return '.'
  #elif c==Cell.b:  return '*'
  #elif c==Cell.w:  return '@'
  #elif c==Cell.bw: return '-'
  #else: assert(False)

def char_to_cell(c): return Cell_chars.index(c)

class Hexstate:
#  board encircled with rings: top/btm black, sides white
#    must be at least one ring

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
    self.brd[Rings + row][Rings + col] = color

  def __init__(self, rows, cols):
    Rings = 1 # number of ringsding rings around board
    assert(Rings > 0)
    self.r, self.c, self.bsize =  rows, cols, (2*Rings+rows)*(2*Rings+cols)
    # all empty cells to start
    self.brd = np.array([[Cell.e]*(2*Rings+cols)] *(2*Rings+rows), dtype = np.int8)
    # set cells in outer rings
    for j in range(self.brd.shape[0]):
      for k in range(self.brd.shape[1]):
        if (j < Rings) or (j>= Rings + rows):
          if (k < Rings) or (k>= Rings + cols):
            self.brd[j][k] = Cell.bw
          else:
            self.brd[j][k] = Cell.b
        elif (k< Rings) or (k >= Rings + cols):
          self.brd[j][k] = Cell.w

  def showboard(self):
    rowlabelfield = '  '
    pretty = '\n' + rowlabelfield
    pretty += '  ' * (Rings-1) + ' '
    for c in range(self.c): 
      pretty += ' ' + chr(ord('a')+c)
    pretty += '\n'
    for j in range(self.brd.shape[0]):
      pretty += j*' '
      if j < Rings or j >= Rings + self.r:
        pretty += rowlabelfield
      else:
        if j+1-Rings < 10:
          pretty += ' ' + str(j+1 - Rings)
        else:
          pretty +=       str(j+1 - Rings)
      for k in range(self.brd.shape[1]):
        pretty += ' ' + cell_to_char(self.brd[j][k])
      pretty += '\n'
    print(pretty)

  def genmove(self, cmd):
    assert(cmd[0][0]=='g')
    cmd = cmd.split()
    if len(cmd)==2 and (char_to_cell(cmd[1][0]) == Cell.b or   
                        char_to_cell(cmd[1][0]) == Cell.w):
      print(' genmove coming soon')
    else:
      print(' invalid genmove request')

  def makemove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if char_to_cell(ch) == Cell.b or char_to_cell(ch) == Cell.w:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < self.r and y>=0 and y < 1+self.c:
            self.putstone(x, y, char_to_cell(ch))
            return
          else: print('\n  coordinate off board')
    print('\n  ... please try again ...\n')

def printmenu():
  print('\n  u          undo last move')
  print('  z x y      boardsize x y')
  print('  * b8       play * b 8')
  print('  o e11      play o e 11')
  print('  g b/w      genmove')
  print('  [return]          quit')

def playgame():
  def boardsizerequest(h, cmd):
    cmd = cmd.split()
    if len(cmd)==3 and cmd[1].isdigit() and cmd[2].isdigit():
      x, y = int(cmd[1]), int(cmd[2])
      if x>0 and y>0 and x<20 and y<20:
        return Hexstate(x,y)
    print('\n invalid boardsize request\n')
    return h

  h = Hexstate(2,3)
  printmenu()
  while True:
    h.showboard()
    if h.gameover():
      print('\n game over ... who won ? \n')
      return
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      print('undo coming soon')
    elif cmd[0][0]=='g':
      h.genmove(cmd)
    elif cmd[0][0]=='z':
      h = boardsizerequest(h, cmd)
    else:
      h.makemove(cmd)

playgame()
