"""
vc-mustplay small-board hex solver

ok up to 4x4 boards
TODO: add captured cell reasoning
TODO: use H-search to find vcs

based on hex-simple.py
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

index positions for     board:    0 1 2       <- row 0
                                   3 4 5       <- row 1
                                    6 7 8       <- row 2
"""

def coord_to_point(r, c, C): 
  return c + r*C

def point_to_coord(p, C): 
  return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def pointset_to_str(S):
  s = ''
  for j in range(N):
    s += BCH if j in S else ECH
  return s

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

class Position: # hex board 
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
set board size 
"""

ROWS = 4
COLS = 4
N = ROWS * COLS

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
print(LFT_COL, RGT_COL, TOP_ROW, BTM_ROW)

"""
cell order determines move order
"""

if ROWS == 2 and COLS == 2: CELLS = (1,2,0,3)
elif ROWS == 3 and COLS == 3: CELLS = (4,2,6,3,5,1,7,0,8)
elif ROWS == 3 and COLS == 4: CELLS = (5,6,4,7,2,9,3,8,1,10,0,11)
elif ROWS == 4 and COLS == 4: CELLS = (6,9,3,12,2,13,5,10,8,7,1,14,4,11,0,15)
elif ROWS == 5 and COLS == 5: 
    CELLS = (12,8,16,7,17,6,18,11,13,4,20,3,21,2,22,15,9,10,14,5,19,1,23,0,24)
else: CELLS = [j for j in range(N)]  # this order terrible for solving

"""
input, output
"""

def char_to_color(c): 
  return PTS.index(c)

escape_ch           = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors         = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

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
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]])
    pretty += '\n'
  print(pretty)

def undo(H, brd):  # pop last meta-move
  if len(H)==1:
    print('\n    original position,  nothing to undo\n')
    return brd
  else:
    H.pop()
    return copy.copy(H[len(H)-1])

def msg(s, ch):
  if has_win(s, 'x'): return('x has won')
  elif has_win(s, 'o'): return('o has won')
  else: 
    wm, calls, vc = win_move(s, ch)
    out = '\n' + ch + '-to-move: '
    out += (ch if wm else oppCH(ch)) + ' wins' 
    out += (' ... ' if wm else ' ') + wm + '\n'
    out += str(calls) + ' calls   '
    out += pointset_to_str(vc)
    return out

"""
solving
"""

def has_win(brd, who):
  set1, set2 = (TOP_ROW, BTM_ROW) if who == BCH else (LFT_COL, RGT_COL)
  #print('has_win', brd, who, set1, set2)
  Q, seen = deque([]), set()
  for c in set1:
    if brd[c] == who: 
      Q.append(c)
      seen.add(c)
  while len(Q) > 0:
    c = Q.popleft()
    if c in set2: 
      return True
    for d in NBRS[c]:
      if brd[d] == who and d not in seen:
        Q.append(d)
        seen.add(d)
  return False

def win_move(s, ptm): # assume neither player has won yet
  """
  s        board, as string
  ptm      player to move, as character
  return   winning move if ptm has winning move, else ''
           count   total number of calls 
           win_set virtual connection for winner
             if ptm:  win_move U win_set is ptm winning s-c
             if op't:            win_set is opt winning v-c
  """
  #print('win_move', s, ' ', ptm)
  optm = oppCH(ptm)

  calls, win_set = 1, set()
  mustplay, opt_win_threats = set(), []
  for j in CELLS:
    if s[j]==ECH: mustplay.add(j)
  #print('mustplay ', mustplay)

  while len(mustplay) > 0:
    for move in CELLS:
      if move in mustplay: break
    t = change_str(s, move, ptm) # resulting board
    if has_win(t, ptm):
      return point_to_alphanum(move, COLS), calls, {move}
    omv, ocalls, oset = win_move(t, optm)
    calls += ocalls
    if not omv: # opponent has no winning response to ptm move
      oset.add(move)
      return point_to_alphanum(move, COLS), calls, oset
    mustplay = mustplay.intersection(oset)
    opt_win_threats.append(oset)
  ovc = set.union(*opt_win_threats)
  return '', calls, ovc

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
