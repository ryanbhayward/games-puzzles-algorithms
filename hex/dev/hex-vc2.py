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
                               TOP 9 

board index positions:            0 1 2           <- row 0
                           RGT 11  3 4 5  LFT 12   <- row 1
                                    6 7 8           <- row 2

                                     BTM 10
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
INF = N+1  # upper-bound on side-to-side distance
TOP, BTM, LFT, RGT = N, N+1, N+2, N+3

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
top, btm, lft, rgt = [], [], [], []
for c in range(COLS): 
  top.append(coord_to_point(0, c, COLS))
  btm.append(coord_to_point(ROWS-1, c, COLS))
for r in range(ROWS): 
  lft.append(coord_to_point(r, 0, COLS))
  rgt.append(coord_to_point(r, COLS-1, COLS))
for j in [top, btm, lft, rgt]:
  NBRS.append(j)
#print('nbrs', NBRS)

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
  hwx = has_win(s, 'x')
  if hwx[0]: 
    return('x has won')
  hw = has_win(s, 'o')
  if hw[0]: 
    return('o has won')
  else: 
    h1 = hwx[1] if ch=='x' else hw[1]
    wm, calls, vc = win_move(s, ch, h1)
    out = '\n' + ch + '-to-move: '
    out += (ch if wm else oppCH(ch)) + ' wins' 
    out += (', ' if wm else ' ') + wm + '\n'
    out += str(calls) + ' calls   '
    out += pointset_to_str(vc)
    return out

"""
solving
"""

def has_win(brd, who): # use double distance to check for win
  start = (TOP, BTM) if who == BCH else (LFT, RGT)
  D = (np.full((2,N+4), INF, dtype = np.int8))
  for j in range(2):
    for k in range(4): 
      D[j][N+k] = 0
    Q = deque([start[j]])
    while len(Q) > 0:
      c = Q.popleft()
      for z in NBRS[c]:
        if brd[z] == who and D[j][z] == INF:
          Q.appendleft(z)
          D[j][z] = D[j][c]
        if brd[z] == ECH and D[j][z] == INF:
          Q.append(z)
          D[j][z] = D[j][c] + 1
  #  print(D[j])
  dist = [sum(x) for x in zip(D[0],D[1])][0:N]
  #print(who, ' hw ', brd,'\n')
  #for j in dist: print(j, end=' ')
  #print()
  ordered = np.argsort(dist)
  #for j in ordered: print(j, end=' ')
  #print()
  return dist[ordered[0]] == 0, ordered

def win_move(s, ptm, ordered): # assume neither player has won yet
  """
  s        board, as string
  ptm      player to move, as character
  ordered  cells by double_distance_order
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
  for j in range(N):
    if s[j]==ECH: 
      mustplay.add(j)
  if len(mustplay)==0:
    print(s)
    print(ptm)
    print(ordered)
    assert(False)
  while len(mustplay) > 0:
    for move in ordered:
      if move in mustplay: break
    t = change_str(s, move, ptm) # resulting board
    hw = has_win(t, ptm)
  #  print(t, ' ', hw[0], ' ', hw[1])
    if hw[0]:
      return point_to_alphanum(move, COLS), calls, {move}
    omv, ocalls, oset = win_move(t, optm, hw[1])
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
