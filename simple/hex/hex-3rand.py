"""
for 3x3 uniform-random hex, over all permutations,
  compute probability that game ends after k moves

answer:
 move 1: 0
 move 2: 0
 move 3: 0
 move 4: 0
 move 5: 2/21
 move 6: 2/21
 move 7: 5/21
 move 8: 5/21
 move 9: 7/21 = 1/3
"""

import numpy as np
import copy
from collections import deque
from itertools import permutations as perms
from math import factorial as fact

"""
points on the board
"""

PTS = '.xo'
EMPTY, BLACK, WHITE = 0, 1, 2
ECH, BCH, WCH = PTS[EMPTY], PTS[BLACK], PTS[WHITE]

def oppCH(ch): 
  if ch==BCH: return WCH
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
  return 'abcdefghj'[c] + '1234566789'[r]

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

ROWS = 3
COLS = 3
N = ROWS * COLS
assert(ROWS == 3 and COLS ==3)

NBRS = []
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

class Position: # 3x3 hex board 
  def __init__(self, rows, cols):
    self.R, self.C, self.n = rows, cols, rows*cols
    self.brd = PTS[EMPTY]*self.n

"""
input, output
"""

def char_to_color(c): 
  return PTS.index(c)

escape_ch = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

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

def play_perms():
  p = Position(ROWS,COLS)
  L = perms(['0','1','2','3','4','5','6','7','8'])
  dim = ROWS*COLS
  fact9 = fact(9)
  wins = [0]*dim
  print(wins)
  for prm in L:
    #print(prm)
    #showboard(p.brd, p.R, p.C)
    stone = BCH
    p.brd = '.'*dim
    for j in range(dim):
      p.brd = change_str(p.brd, int(prm[j]), stone)
      #showboard(p.brd, p.R, p.C)
      if has_win(p.brd, stone):
        wins[j] += 1
        break
      stone = oppCH(stone)
  print(wins)
  for j in range(dim):
    print(j, wins[j], wins[j] / fact9)

play_perms()
