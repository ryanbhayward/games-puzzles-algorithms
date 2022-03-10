"""
3-3 hex program, based on ttt and 3x3 go programs RBH 2019
"""

import numpy as np
import copy
from collections import deque

"""
points on the board
"""

PTS = '.xo'
EMPTY, BLACK, WHITE = 0, 1, 2
ECH, BCH, WCH = PTS[EMPTY], PTS[BLACK], PTS[WHITE]

def oppCH(ch): 
  if ch== BCH: return WCH
  elif ch== WCH: return BCH
  else: assert(False)

"""
board: one-dimensional string

index positions for     board:    6 7 8       <- row 2
                                   3 4 5       <- row 1
                                    0 1 2       <- row 0
"""

def coord_to_point(r, c, C): 
  return c + r*C

def point_to_coord(p, C): 
  return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '123456789'[r]

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

ROWS = 3
COLS = 3
N = ROWS * COLS
assert(ROWS == 3 and COLS ==3)

NBRS = []  # neighbours
for r in range(ROWS):
  for c in range(COLS):
    nbs = []
    if r > 0:                nbs.append(coord_to_point(r-1, c,   COLS))
    if r > 0 and c < COLS-1: nbs.append(coord_to_point(r-1, c+1, COLS))
    if c > 0:                nbs.append(coord_to_point(r,   c-1, COLS))
    if c < COLS-1:           nbs.append(coord_to_point(r,   c+1, COLS))
    if r < ROWS-1 and c > 0: nbs.append(coord_to_point(r+1, c-1, COLS))
    if r < ROWS-1:           nbs.append(coord_to_point(r+1, c, COLS))
    NBRS.append(nbs)
#print('nbrs', NBRS)

LFT_COL, RGT_COL, TOP_ROW, BTM_ROW = set(), set(), set(), set()

for r in range(ROWS):
  LFT_COL.add(coord_to_point(r, 0, COLS))
  RGT_COL.add(coord_to_point(r, COLS-1, COLS))

for c in range(COLS):
  TOP_ROW.add(coord_to_point(0, c, COLS))
  BTM_ROW.add(coord_to_point(ROWS-1, c, COLS))

#print(LFT_COL, RGT_COL, TOP_ROW, BTM_ROW)

"""
for 3x3 board, we can check each of the 11 possible minimal paths directly,
instead of using a bfs, or using the union-find algorithm
"""

def has_win(s, p): # for 3x3 board only
  if p == BCH:
    return \
    (s[0]==BCH) and (s[3]==BCH) and (s[6]==BCH) or \
    (s[1]==BCH) and (s[4]==BCH) and (s[7]==BCH) or \
    (s[2]==BCH) and (s[5]==BCH) and (s[8]==BCH) or \
    (s[1]==BCH) and (s[3]==BCH) and (s[6]==BCH) or \
    (s[2]==BCH) and (s[4]==BCH) and (s[7]==BCH) or \
    (s[2]==BCH) and (s[4]==BCH) and (s[6]==BCH) or \
    (s[1]==BCH) and (s[4]==BCH) and (s[6]==BCH) or \
    (s[2]==BCH) and (s[5]==BCH) and (s[7]==BCH) or \
    (s[0]==BCH) and (s[3]==BCH) and (s[4]==BCH) and (s[7]==BCH) or \
    (s[1]==BCH) and (s[4]==BCH) and (s[5]==BCH) and (s[8]==BCH) or \
    (s[0]==BCH) and (s[3]==BCH) and (s[4]==BCH) and (s[5]==BCH) and (s[8]==BCH)
  return \
    (s[0]==WCH) and (s[1]==WCH) and (s[2]==WCH) or \
    (s[3]==WCH) and (s[4]==WCH) and (s[5]==WCH) or \
    (s[6]==WCH) and (s[7]==WCH) and (s[8]==WCH) or \
    (s[3]==WCH) and (s[1]==WCH) and (s[2]==WCH) or \
    (s[6]==WCH) and (s[4]==WCH) and (s[5]==WCH) or \
    (s[2]==WCH) and (s[4]==WCH) and (s[6]==WCH) or \
    (s[3]==WCH) and (s[4]==WCH) and (s[2]==WCH) or \
    (s[6]==WCH) and (s[7]==WCH) and (s[5]==WCH) or \
    (s[0]==WCH) and (s[1]==WCH) and (s[4]==WCH) and (s[5]==WCH) or \
    (s[3]==WCH) and (s[4]==WCH) and (s[7]==WCH) and (s[8]==WCH) or \
    (s[0]==WCH) and (s[1]==WCH) and (s[4]==WCH) and (s[7]==WCH) and (s[8]==WCH)

def can_win(s, ptm): # assume neither player has won yet
  blanks, calls = [], 1
  #for j in range(N):
  #for j in (0, 1, 2, 3, 4, 5, 6, 7, 8): # natural order
  for j in (4, 2, 6, 3, 5, 1, 7, 0, 8): # better 3x3 move order
    if s[j]==ECH: blanks.append(j)
  #if len(blanks)==0: print('whoops',s)
  #assert(len(blanks)>0) # since x has no draws
  optm = oppCH(ptm)
  for k in blanks:
    t = change_str(s, k, ptm)
    if has_win(t, ptm):
      return True, calls
    cw, prev_calls = can_win(t, optm)
    calls += prev_calls
    if not cw:
      return True, calls
  return False, calls

class Position: # 3x3 hex board 
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

escape_ch = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

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
  for j in range(R): # rows
    pretty += ' ' + ' '*j + paint(str(1+j)) + ' '
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
    #print('\n   removing position ', H.pop())
    H.pop()
    return copy.copy(H[len(H)-1])

def msg(s, ch):
  if has_win(s, 'x'): return('x wins')
  elif has_win(s, 'o'): return('o wins')
  else: 
    cw, calls = can_win(s, ch)
    out = ch + '-to-move ?  ' + \
      (ch if cw else oppCH(ch)) + ' can win, ' + str(calls) + ' calls\n'
    return out

def interact():
  p = Position(ROWS, COLS)
  history = []  # board positions
  new = copy.copy(p.brd); history.append(new)
  while True:
    showboard(p.brd, p.R, p.C)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      p.brd = undo(history, p.brd)
    elif cmd[0][0]=='?':
      cmd = cmd.split()
      if len(cmd)>0:
        if cmd[1][0]=='x': 
          print(msg(p.brd, 'x'))
        elif cmd[1][0]=='o': 
          print(msg(p.brd, 'o'))
    elif (cmd[0][0] in PTS):
      new = p.requestmove(cmd)
      if new != '':
        p.brd = new
        history.append(new)

interact()
