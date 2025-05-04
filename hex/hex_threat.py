"""
modified hex_simple to allow Van Rijswijck's threat search
2025 rbh
"""

import copy
from collections import deque
import time
from menu import printmenu

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

def coord_to_point(r, c, C): return c + r*C

def point_to_coord(p, C): return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

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

ROWS, COLS = 4, 4
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
#print(LFT_COL, RGT_COL, TOP_ROW, BTM_ROW)

"""
cell order determines move order
"""

CELLS = range(N)  # this order terrible for solving
#if ROWS == 2 and COLS == 2: CELLS = (1,2,3,0)
#if ROWS == 3 and COLS == 3: CELLS = (4,2,6,3,5,1,7,0,8)
#if ROWS == 3 and COLS == 4: CELLS = (0,1,2,3,4,5,6,7,8,9,10,11)
#if ROWS == 3 and COLS == 4: CELLS = (5,6,4,7,2,9,3,8,1,10,0,11)
#if ROWS == 3 and COLS == 4: CELLS = (5,9,10,3,8,1,4,6,2,7,0,11)
#if ROWS == 4 and COLS == 3: CELLS = (4,7,5,6,3,2,8,9,1,10,0,11)
if ROWS == 4 and COLS == 4: CELLS = (6,9,3,12,2,13,5,10,8,7,1,14,4,11,0,15)

"""
input, output
"""

def char_to_color(c): 
  return PTS.index(c)

escape_ch           = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors         = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

#def printmenu():
#  print('  h             help menu')
#  print('  x b2         play x b 2')
#  print('  o e3         play o e 3')
#  print('  . a2          erase a 2')
#  print('  u                  undo')
#  print('  [return]           quit')

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
  if has_win(s, 'x'): 
    return('x has won')
  elif has_win(s, 'o'): return('o has won')
  else: 
    start_time = time.time()
    #wm, calls = mmx_move(s, ch)
    #out = '\n' + ch + '-to-move: '
    #out += (ch if wm else oppCH(ch)) + ' wins' 
    #out += (' ... ' if wm else ' ') + wm + '\n'
    #out += str(calls) + ' calls\n'
    #out += format(time.time() - start_time, '.2f') + ' seconds\n'
    
    mp = empty_cells(s, CELLS)
    ptm_wins, winmv, winset, calls = th_search(0, s, ch, mp)
    print(ptm_wins, winmv, winset, calls)
    print('CELLS', CELLS)

    #return out
    return ''

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

def mmx_move(s, ptm): # assumes no winner yet
  calls = 1 # count total number of calls
  optm = oppCH(ptm)
  for k in CELLS: # for every cell on the board
    if s[k]==ECH:   # if the cell is empty
      t = change_str(s, k, ptm) # ptm plays at cell k
      if has_win(t, ptm): # did this move win for ptm?
        return point_to_alphanum(k, COLS), calls
      # if not, continue from new board t with optm
      optm_wins, prev_calls = mmx_move(t, optm)
      calls += prev_calls
      # if optm has no winning move, then
      #   ptm move at k is a winning move
      if not optm_wins:
        return point_to_alphanum(k, COLS), calls
  return '', calls

def empty_cells(psn, L):
  E = []
  for j in L:
    if psn[j] == ECH: 
      E.append(j)
  return set(E)

def next_cell(mp, L): # remove 1st item in CELLS from mp
  for j in L:
    if j in mp: 
     mp.remove(j)
     return j

def move_to_front(x, L):
  assert(x in L)
  M = [x]
  for j in L:
    if j != x:
      M.append(j)
  return tuple(M)

def th_search(d, s, ptm, mp): # return ptm_wins?, winmove_if_yes, carrier, calls
# carrier is cell set of winning player's strategy
  global CELLS
  if d <= 0: print('  '*d, s, 'start', ptm, mp)
  calls, optm = 1, oppCH(ptm)
  union_threats = set() # union of carriers of all opponent win-threats
  while mp: # False if mp is empty
    k = next_cell(mp, CELLS)
    if d <= 0: print('  '*d, 'try', k)
    t = change_str(s, k, ptm)
    if has_win(t, ptm):
      CELLS = move_to_front(k, CELLS)
      if d <= 0: print('  '*d, s, 'finish', ptm, 'wins', mp, 'winset', set([k]))
      return True, k, set([k]), calls
    move_list = empty_cells(t, CELLS)
    optm_wins, owinmv, winset, prev_calls = th_search(d+1, t, optm, move_list)
    calls += prev_calls
    if not optm_wins: 
      CELLS = move_to_front(k, CELLS)
      winset.add(k)
      if d <= 0: print('  '*d, s, 'finish', ptm, 'wins', mp, 'winset', winset)
      return True, k, winset, calls
    if d <= 0: print('  '*d, s, 'opponent threat', owinmv, winset)
    # optm wins, refine mustply
    CELLS = move_to_front(owinmv, CELLS)
    mp = mp.intersection(winset)
    union_threats = union_threats.union(winset)
  if d <= 0: print('  '*d, s, 'finish', ptm, 'loses', mp, 'winset', union_threats)
  return False, None, union_threats, calls

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
    elif cmd[0][0]=='r':
      for ch in (BCH, WCH):
        r = set()
        rn = reachable(p.brd, ch, r)
        assert(rn==len(r))
        print(rn, ch, 'reachable nodes')
        print(TOAC(p.brd, ch), ch, 'TOAC nodes')
    elif cmd[0][0]=='?':
      cmd = cmd.split()
      if len(cmd)>0:
        for ch in (BCH, WCH):
          if cmd[1][0]==ch: 
            print(msg(p.brd, ch))
    elif (cmd[0][0] in PTS):
      new = p.requestmove(cmd)
      if new != '':
        p.brd = new
        history.append(new)

interact()
