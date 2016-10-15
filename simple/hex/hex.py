# simple hex player RBH 2016
import numpy as np
from random import shuffle

# global constants
Rings      = 1  # wrapping around the playing board
Cell_chars = '*@-.'
escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor,\
               textcolor)

class Cell():  # black, white, blackwhite (dead), empty
  b, w, bw, e  = 0, 1, 2, 3
  
def cell_to_char(n): 
  return Cell_chars[n]

def char_to_cell(c): 
  return Cell_chars.index(c)

def paint(string):
  if len(string)>1 and string[0]==' ': 
   return ' ' + paint(string[1:])
  x = Cell_chars.find(string[0])
  if x >= 0:
    return stonecolors[x] + string + colorend
  elif string.isalnum():
    return textcolor + string + colorend
  return string

class Hexstate:
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
    self.brd[Rings + row][Rings + col] = color

  def __init__(self, rows, cols):
    assert(Rings > 0)
    self.r, self.c, self.bsize =  rows, cols, (2*Rings+rows)*(2*Rings+cols)
    self.brd = np.array(  # to start, all empty
      [[Cell.e]*(2*Rings+cols)] *(2*Rings+rows), dtype = np.int8)
    # non-empty values
    for j in range(self.brd.shape[0]):
      for k in range(self.brd.shape[1]):
        if (j < Rings and k < Rings + cols) or \
           (j >= Rings + rows and k >= Rings):
          self.brd[j][k] = Cell.b
        elif (k < Rings and j >= Rings) or \
             (k >= Rings + cols and j <= Rings + rows):
          self.brd[j][k] = Cell.w

  def showboard(self):
    rowlabelfield = '  '
    pretty = '\n' + rowlabelfield
    pretty += '  ' * (Rings-1) + ' '
    for c in range(self.c): 
      pretty += ' ' + paint(chr(ord('a')+c))
    pretty += '\n'
    for j in range(self.brd.shape[0]):
      pretty += j*' '
      if j < Rings or j >= Rings + self.r:
        pretty += rowlabelfield
      else:
        pretty += paint('{:2}'.format(j+1-Rings))
      for k in range(self.brd.shape[1]):
        pretty += ' ' + paint(cell_to_char(self.brd[j][k]))
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
