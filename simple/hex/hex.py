# simple hex player RBH 2016

from random import shuffle
from sys import stdin
from copy import deepcopy

class Hexstate:
#  board is string, padded with 
#    black at top
#    white on sides
#    2 files of offboard markers

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
    return (row+2)*(self.c+4) + col + 2

  def gameover(self):
    return False

  def putstone(self, row, col, ch):
    p = self.psn(row,col)
    self.brd = self.brd[0:p] + ch + self.brd[p+1:]

  def __init__(self, rows, cols):
    self.r, self.c, self.bsize =  rows, cols, (rows+4)*(cols+4)
    self.chBW, self.chB, self.chW, self.chE = '-', '*', 'o', '.'
    self.brd = ''
    self.brd += (self.chBW * 2 + self.c * self.chB + self.chBW * 2) * 2
    self.brd += (self.chW  * 2 + self.c * self.chE + self.chW  * 2) * self.r
    self.brd += (self.chBW * 2 + self.c * self.chB + self.chBW * 2) * 2

  def showboard(self):
    pretty, row = '\n', 0
    for j in range(self.bsize):
      pretty += self.brd[j] + ' '
      if j%(4+self.c) == 3+self.c: 
        row += 1
        pretty += '\n' + ' '*row
    print(pretty)

  def makemove(self, cmd):
    if len(cmd) != 3: 
      print('\n  move needs 3 param\n')
      return
    ch = cmd[0][0]
    if   ch=='b': ch = self.chB
    elif ch=='w': ch = self.chW
    else:
      print('b ?  w?  try again')
      return
    self.putstone(int(cmd[1])-1, int(cmd[2])-1, ch)

def printmenu():
  print('game commands')
  print('  b x y    black to (x y)')
  print('  w x y    white to (x y)')
  print('  ? b/w    genmove black/white')
  print('  h        help -- print this menu')
  print('  [return]          quit')

def playgame():
  h = Hexstate(5,5)
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
      h.showboard()
    #elif cmd[0][0]=='?':
    #  nimdpreport(g)
    else:
      cmd = cmd.split()
      h.makemove(cmd)

playgame()

h = Hexstate(3,3)
h.showboard()
h = Hexstate(4,7)
h.showboard()
for c in (h.chB, h.chW, h.chBW, h.chE):
  h.putstone(2,2,c)
  h.showboard()
