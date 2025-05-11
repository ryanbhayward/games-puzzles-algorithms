"""
rbh 2025
boolean negamax hex solver
4x4 empty board, x-to-move, x wins, 7034997 calls
"""

import hx
import time
from collections import deque

"""
solving
"""

def has_win(brd, who):
  set1, set2 = (hx.TOP_ROW, hx.BTM_ROW) if who == hx.BCH \
          else (hx.LFT_COL, hx.RGT_COL)
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
    for d in hx.NBRS[c]:
      if brd[d] == who and d not in seen:
        Q.append(d)
        seen.add(d)
  return False

def mmx_move(s, ptm): # assumes no winner yet
  calls = 1 # count total number of calls
  optm = hx.Cell.oppCH(ptm)
  for k in hx.CELLS: # for every cell on the board
    if s[k] == hx.ECH: # if cell empty
      t = hx.color_cell(s, k, ptm) # ptm plays at cell k
      if has_win(t, ptm): # did this move win for ptm?
        return hx.point_to_alphanum(k, hx.COLS), calls
      # if not, continue from new board t with optm
      optm_wins, prev_calls = mmx_move(t, optm)
      calls += prev_calls
      # if optm has no winning move, then
      #   ptm move at k is a winning move
      if not optm_wins:
        return hx.point_to_alphanum(k, hx.COLS), calls
  return '', calls

def msg(s, ch):
    if has_win(s, 'x'):
      return('x has won')
    elif has_win(s, 'o'): return('o has won')
    else:
      start_time = time.time()
      wm, calls = mmx_move(s, ch)
      out = '\n' + ch + '-to-move: '
      out += (ch if wm else hx.Cell.oppCH(ch)) + ' wins'
      out += (' ... ' if wm else ' ') + wm + '\n'
      out += str(calls) + ' calls\n'
      out += format(time.time() - start_time, '.2f') + ' seconds\n'
      return out

def interact():
  p = hx.Position(hx.ROWS, hx.COLS)
  history = []  # board positions
  new = hx.copy.copy(p.brd); history.append(new)
  while True:
    hx.IO.showboard(p.brd, p.R, p.C)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      p.brd = undo(history, p.brd)
    elif cmd[0][0]=='r':
      for ch in (hx.BCH, hx.WCH):
        r = set()
        rn = reachable(p.brd, ch, r)
        assert(rn==len(r))
        print(rn, ch, 'reachable nodes')
        print(TOAC(p.brd, ch), ch, 'TOAC nodes')
    elif cmd[0][0]=='?':
      cmd = cmd.split()
      if len(cmd)>0:
        for ch in (hx.BCH, hx.WCH):
          if cmd[1][0]==ch: 
            print(msg(p.brd, ch))
    elif (cmd[0][0] in hx.IO_CH):
      new = p.requestmove(cmd)
      if new != '':
        p.brd = new
        history.append(new)

interact()
