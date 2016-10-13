# simple hex player RBH 2016

from random import shuffle
from sys import stdin
from copy import deepcopy

class Hexstate:
#  board is string, padded with 
#    black at top
#    white on sides
#    pad (currently 2) rings of offboard markers

#  @@******@@
#   @@******@@
#    oo......oo
#     oo......oo
#      oo......oo
#       oo......oo
#        oo......oo
#         oo......oo
#          @@******@@
#           @@******@@
  def psn(self, row, col):
    return (self.pad + row)*(2*self.pad + self.c) + self.pad + col

  def gameover(self):
    return False

  def putstone(self, row, col, ch):
    p = self.psn(row,col)
    self.brd = self.brd[0:p] + ch + self.brd[p+1:]

  def __init__(self, rows, cols):
    self.pad = 1 # number of padding rings around board
    assert(self.pad > 0)
    self.r, self.c, self.bsize =  rows, cols, (2*self.pad+rows)*(2*self.pad+cols)
    # cell can be black, white, blackwhite (both), empty
    self.chBW, self.chB, self.chW, self.chE = '-', '*', 'o', '.'
    self.brd = ''
    # top rows (padding)
    self.brd += (self.chBW * self.pad + self.c * self.chB + self.chBW * self.pad) * self.pad
    # next rows 
    self.brd += (self.chW  * self.pad + self.c * self.chE + self.chW  * self.pad) * self.r
    # bottom rows (padding)
    self.brd += (self.chBW * self.pad + self.c * self.chB + self.chBW * self.pad) * self.pad

  def showboard(self):
    rowlabelfield = '   '
    pretty, row = '\n ' + rowlabelfield, 0
    for c in range(self.c):   
      pretty += ' ' + chr(ord('a')+c)
    pretty += '\n' + rowlabelfield
    for j in range(self.bsize):
      pretty += self.brd[j] + ' '
      if j%(2*self.pad + self.c) == (2*self.pad - 1) + self.c: 
        row += 1
        pretty += '\n' + ' '*row
        rowonboard = 1 + row - self.pad
        if rowonboard > self.r: pretty += rowlabelfield
        if rowonboard > 0 and rowonboard <= self.r:
          if rowonboard < 10 and self.r >= 10:
            pretty += ' ' + str(rowonboard) + ' '
          else:           
            pretty +=       str(rowonboard) + ' '
    print(pretty)

  def genmove(self, cmd):
    assert(cmd[0][0]=='g')
    cmd = cmd.split()
    if len(cmd)==2 and (cmd[1][0]=='b' or cmd[1][0]=='w'):
      print(' genmove coming soon')
    else:
      print(' invalid genmove request')

  def makemove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch== self.chB or ch==self.chW:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < self.r and y>=0 and y < 1+self.c:
            self.putstone(x, y, ch)
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

  h = Hexstate(5,3)
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
