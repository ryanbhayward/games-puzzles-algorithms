"""
looks like I used this to count legal go positions on small boards RBH 2019
looks similar to go_play.py
"""

import numpy as np
import itertools
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
board
"""

ROWS, COLS = 2,2
N = ROWS * COLS

"""
board: one-dimensional string

index positions for 2x3 board:    3 4 5       <- row 1
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
    self.cells = np.array([j for j in range(self.n)], np.dtype(np.int8))
    self.brd = PTS[EMPTY]*self.n
    self.nbrs = []
    for r in range(rows):
      for c in range(cols):
        nbs = []
        if r > 0:        nbs.append(coord_to_point(r-1, c,  cols))
        if r < rows - 1: nbs.append(coord_to_point(r+1, c,  cols))
        if c > 0:        nbs.append(coord_to_point(r,  c-1, cols))
        if c < cols - 1: nbs.append(coord_to_point(r,  c+1, cols))
        self.nbrs.append(nbs)

  def legal_psn(self):
    seen = set()
    for c in range(self.n):
      if c not in seen and self.brd[c] != ECH:
        seen.add(c)
        has_liberty = False
        q = deque([c])
        while len(q)>0:
          v = q.pop()
          for w in self.nbrs[v]:
             if self.brd[w]==ECH:
               has_liberty = True
             elif self.brd[w]==self.brd[v] and w not in seen:
               seen.add(w)
               q.appendleft(w)
        if not has_liberty: return False
    return True

  def tromp_taylor_score(self):
    bs, ws, empty_seen = 0, 0, set()
    for p in range(self.n):
      if   self.brd[p] == BCH: bs += 1
      elif self.brd[p] == WCH: ws += 1
      elif (self.brd[p] == ECH) and (p not in empty_seen):
        b_nbr, w_nbr = False, False
        empty_seen.add(p)
        empty_points = [p]
        territory = 1
        while (len(empty_points) > 0):
          q = empty_points.pop()
          for x in self.nbrs[q]:
            b_nbr |= (self.brd[x] == BCH)
            w_nbr |= (self.brd[x] == WCH)
            if self.brd[x] == ECH and x not in empty_seen:
              empty_seen.add(x)
              empty_points.append(x)
              territory += 1
        if   b_nbr and not w_nbr: bs += territory
        elif w_nbr and not b_nbr: ws += territory
    return bs, ws

  def captured(self, brd, whr, color):
  # return list: group containing whr if captured, empty if not captured
    assert(brd[whr] == color)
    j, points = 0, [whr]
    while (j < len(points)): # breadth-first-search
      p = points[j]
      for q in self.nbrs[p]:
        if brd[q] == ECH: # group has liberty, not captured
          return []
        if (brd[q] == color) and (q not in points):
          points.append(q)
      j += 1
    # group is captured
    return points

  def put_and_capture(self, where, color):
    assert(self.brd[where] == ECH)
    t, did_cap = change_str(self.brd, where, color),  False
    for w in self.nbrs[where]:
      cap = []
      if t[w] == oppCH(color):
        cap += self.captured(t, w, oppCH(color))
        if (len(cap)>0):
          did_cap = True
          print('removing captured group at', point_to_alphanum(w, self.C))
          for j in cap:
            t = change_str(t, j, ECH)
    if did_cap: # no need for suicide check if capture made 
      return t
    #suicide check
    cap = self.captured(t, where, color)
    if (len(cap) > 0):
      print('whoops, no liberty there: move not allowed')
      return ''
    return t

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
    return self.put_and_capture(where, ch)

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
  p = Position(ROWS, COLS)
  #print(p.R, p.C, p.n, coord_to_point(0,0,p.C), coord_to_point(p.R-1,p.C-1,p.C))
  history = []  # board positions
  new = copy.copy(p.brd); history.append(new)
  while True:
    #print(p.brd)
    showboard(p.brd, p.R, p.C)
    for h in history: print(h)
    print('\n')
    print('tromp-taylor score (black, white)',p.tromp_taylor_score(),'\n')
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

def cartesian(n, st):
  if n == 1:
    return [x for x in st]
  return [a + b for a in st for b in cartesian(n-1, st)]

#for j in [a+b+c+d for a in PTS for b in PTS for c in PTS for d in PTS]:
#  print(j)
def count_legal_positions(r,c):
  p = Position(r, c)
  legal = 0
  for p.brd in cartesian(r*c, PTS):
    if p.legal_psn():
      legal += 1
  print(r, 'rows', c, 'cols ', legal, 'legal positions out of ', 3**(r*c))

count_legal_positions(2,2)
count_legal_positions(2,3)
count_legal_positions(3,3)
count_legal_positions(3,4)

#interact()
