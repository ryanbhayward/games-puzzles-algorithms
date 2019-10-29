"""
modified ttt program      RBH 2019
  - game ends **** only **** if x gets 3-in-a-row or board full 
  - x wins **** if and only if **** x has 3-in-a-row

  - based on go program code, so x is BLACK o is WHITE
"""

import numpy as np
import copy

"""
points on the board
"""

PTS = '.xo'
EMPTY, BLACK, WHITE = 0, 1, 2
ECH, BCH, WCH = PTS[EMPTY], PTS[BLACK], PTS[WHITE]

def x_wins(s):
  return (s[0]=='x') and (s[1]=='x') and (s[2]=='x') or \
         (s[3]=='x') and (s[4]=='x') and (s[5]=='x') or \
         (s[6]=='x') and (s[7]=='x') and (s[8]=='x') or \
         (s[0]=='x') and (s[3]=='x') and (s[6]=='x') or \
         (s[1]=='x') and (s[4]=='x') and (s[7]=='x') or \
         (s[2]=='x') and (s[5]=='x') and (s[8]=='x') or \
         (s[0]=='x') and (s[4]=='x') and (s[8]=='x') or \
         (s[2]=='x') and (s[4]=='x') and (s[6]=='x') 

def x_can_win(s, ptm):
  if x_wins(s):
    return True
  blanks = []
  for j in range(9):
    if s[j]==ECH: blanks.append(j)
  if len(blanks)==0:
    return False
  if ptm == BCH:
    for k in blanks:
      t = change_str(s, k, BCH)
      if x_can_win(t, WCH):
        return True
    return False
  # ptm == WCH
  for k in blanks:
    t = change_str(s, k, WCH)
    if not x_can_win(t, BCH):
      return False
  return True

def oppCH(ch): 
  if ch== BCH: return WCH
  elif ch== WCH: return BCH
  else: assert(False)

"""
board
"""

ROWS, COLS = 3, 3
N = ROWS * COLS

"""
board: one-dimensional string

index positions for     board:    6 7 8       <- row 2
                                  3 4 5       <- row 1
                                  0 1 2       <- row 0
                                  | | |
                                  0 1 2       <- columns
"""
def coord_to_point(r, c, C): 
  return c + r*C

def point_to_coord(p, C): 
  return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

class Position: # go board 
  def __init__(self, rows, cols):
    self.R, self.C, self.n = rows, cols, rows*cols
    self.brd = PTS[EMPTY]*self.n

  def requestmove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd) != 2:
      print('invalid command')
      return ''
    ch = cmd[0][0]
    if ch not in PTS:
      print('bad character')
      return ''
    q, n = cmd[1][0], cmd[1][1:]
    if (not q.isalpha()) or (not n.isdigit()):
      print('not alphanumeric')
      return ''
    x, y = int(n) - 1, ord(q)-ord('a')
    if x<0 or x >= self.R or y<0 or y >= self.C:
      print('coordinate off board')
      return ''
    where = coord_to_point(x,y,self.C)
    if self.brd[where] != ECH:
      print('\n  sorry, position occupied')
      return ''
    return change_str(self.brd, where, ch)

"""
input, output
"""

def char_to_color(c): 
  return PTS.index(c)

escape_ch           = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors         = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = PTS.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def printmenu():
  print('  h             help menu')
  print('  x b2         play x b 2')
  print('  o e3         play o e 3')
  print('  . a2          erase a 2')
  print('  u                  undo')
  print('  [return]           quit')

def showboard(brd, R, C):
  def paint(s):  # s   a string
    pt = ''
    for j in s:
      if j in PTS:      pt += stonecolors[PTS.find(j)] + j + colorend
      elif j.isalnum(): pt += textcolor + j + colorend
      else:             pt += j
    return pt

  pretty = '\n   ' 
  for c in range(C): # columns
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(R-1, -1, -1): # rows
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(C): # columns
      #print(coord_to_point(j,k,psn.C), end='')
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]])
    #print('')
    pretty += '\n'
  print(pretty)

def undo(H, brd):  # pop last meta-move
  if len(H)==1:
    print('\n    original position,  nothing to undo\n')
    return brd
  else:
    print('\n   removing position ', H.pop())
    return copy.copy(H[len(H)-1])

def interact():
  p = Position(3,3)
  #print(p.R, p.C, p.n, coord_to_point(0,0,p.C), coord_to_point(p.R-1,p.C-1,p.C))
  history = []  # board positions
  new = copy.copy(p.brd); history.append(new)
  while True:
    showboard(p.brd, p.R, p.C)

    print("\nif it's x's turn: x has ", end='')
    if not x_can_win(p.brd, 'x'): print('not ',end='')
    print('a winning strategy\n')

    if x_wins(p.brd):
      print('x wins\n')
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      p.brd = undo(history, p.brd)
    elif (cmd[0][0] in PTS):
      new = p.requestmove(cmd)
      if new != '':
        if new in history:
          print('superko violation: that move not allowed')
        else:
          p.brd = new
          history.append(new)

interact()
