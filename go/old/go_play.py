#!/usr/bin/env python3
"""
simple Go program  RBH 2019-2022
  * generate legal moves and game score
  * some ideas from M Mueller's go code
  * also allow rectangular boards, so with columns != rows
             1 <= R <= 9 rows 
             1 <= C <= 9 columns
TODO
  * simplify
    - represent board only as string (so numpy not needed)
    - allow board sizes up to 19x19
    - add feature that takes sgf input
    - add feature that reports whether position is legal
"""

import numpy as np
import copy

"""
points on the board
"""

EMPTY, BLACK, WHITE, BORDER, POINT_CHARS = 0, 1, 2, 3, '.*o'

def opponent(color): 
  return BLACK + WHITE - color

"""
the board: a one-dimensional vector of points

to simplify loop computation, add borders (also called guards):
  * a border row at top
  * a border row at bottom
  * a border column at left 
so R x C board requires total (R+2) * (C+1) points:

     3x4 board       points

 g  g  g  g  g   20 21 22 23 24
 g  .  .  .  .   15 16 17 18 19
 g  .  .  .  .   10 11 12 13 14
 g  .  .  .  .    5  6  7  8  9     <= in Go, rows are labelled
 g  g  g  g  g    0  1  2  3  4        from the bottom
"""

def coord_to_point(r, c, C): 
  return (C+1) * (r+1) + c + 1

def point_to_alphanum(p, C):
  r, c = divmod(p, C+1)
  return 'abcdefghi'[c-1] + '1234566789'[r-1]

class Position: # go board with x,o,e point values
  def legal_moves(self):
    L = []
    for j in range(self.n):
      if self.brd[j] == EMPTY: 
        L.append(j)
    return L

  def __init__(self, r, c):
    self.R, self.C = r, c
    self.n, self.fat_n = r * c,  (r+2) * (c+1)
    self.brd = np.full(self.fat_n, BORDER, dtype = np.int8)
    for j in range(self.R):
      for k in range(self.C):
        self.brd[coord_to_point(j,k,self.C)] = EMPTY
    # init nbrs
    self.nbrs = []
    for point in range(self.fat_n):
        if self.brd[point] == BORDER: 
            self.nbrs.append([])
        else:
            nbs = []
            for where in [point-1, point+1, point+self.C+1, point-(self.C+1)]:
              if self.brd[where] != BORDER: 
                  nbs.append(where)
            self.nbrs.append(nbs)

  def brdstring(self):
    b = ''
    for j in self.brd:
      if j != BORDER: b += POINT_CHARS[j]
    return b

  def makemove(self, where, color):
    self.brd[where] = color
    cap = []
    for p in self.nbrs[where]:
      if self.brd[p] == opponent(color):
        cap += self.captured(p, opponent(color))
    if (len(cap)>0):
      print('removing captured group at', point_to_alphanum(where, self.C))
      for j in cap:
        self.brd[j] = EMPTY
      return cap, True
    if self.captured(where, color):
      print('whoops, no liberty there: not allowed')
      self.brd[where] = EMPTY
      return cap, False
    return cap, True

  def requestmove(self, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch in POINT_CHARS:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x<0 or x >= self.R or y<0 or y >= self.C:
            print('\n  sorry, coordinate off board')
            return parseok
          else:
            where = coord_to_point(x,y,self.C)
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
              return parseok
            else:
              color = char_to_color(ch)
              move_record = (color, where)
              print('move record', move_record)
              captured, parseok = self.makemove(where, color)
              if parseok:
                H.append(move_record) # record move for undo
                for x in captured: # record captured stones for undo
                  cap_record = (-opponent(color), x)
                  #print('capture record', cap_record)
                  H.append(cap_record)
              return parseok

  def captured(self, where, color):
  # return points in captured group containing where
  #   empty if group is not captured
    assert(self.brd[where] == color)
    j, points, seen = 0, [where], {where}
    while (j < len(points)):
      p = points[j]
      for q in self.nbrs[p]:
        if self.brd[q] == EMPTY: # group has liberty, not captured
          return []
        if (self.brd[q] == color) and (q not in seen):
          points.append(q)
          seen.add(q)
      j += 1
    # group is captured
    return points

  def tromp_taylor_score(self):
    bs, ws, empty_seen = 0, 0, set()
    for p in range(self.fat_n):
      if   self.brd[p] == BLACK: bs += 1
      elif self.brd[p] == WHITE: ws += 1
      elif (self.brd[p] == EMPTY) and (p not in empty_seen):
        b_nbr, w_nbr = False, False
        empty_seen.add(p)
        empty_points = [p]
        territory = 1
        while (len(empty_points) > 0):
          q = empty_points.pop()
          for x in self.nbrs[q]:
            b_nbr |= (self.brd[x] == BLACK)
            w_nbr |= (self.brd[x] == WHITE)
            if self.brd[x] == EMPTY and x not in empty_seen:
              empty_seen.add(x)
              empty_points.append(x)
              territory += 1
        if   b_nbr and not w_nbr: bs += territory
        elif w_nbr and not b_nbr: ws += territory
    return bs, ws
	        
"""
input, output
"""

def char_to_color(c): 
  return POINT_CHARS.index(c)

escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (textcolor,\
               escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor)

def printmenu():
  print('  h             help menu')
  print('  '+ POINT_CHARS[BLACK] +  ' b2         play BLACK b 2')
  print('  '+ POINT_CHARS[WHITE] +  ' e3         play WHITE e 2')
  print('  u                  undo')
  print('  [return]           quit')

def showboard(psn):
  def paint(s):  # s   a string
    if len(s)>1 and s[0]==' ': 
     return ' ' + paint(s[1:])
    x = POINT_CHARS.find(s[0])
    if x > 0:
      return stonecolors[x] + s + colorend
    elif s.isalnum():
      return textcolor + s + colorend
    return s

  pretty = '\n   ' 
  for c in range(psn.C): # columns
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(psn.R-1, -1, -1): # rows
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(psn.C): # columns
      pretty += ' ' + paint(POINT_CHARS[psn.brd[coord_to_point(j,k,psn.C)]])
    pretty += '\n'
  print(pretty)

def undo(H, brd):  # undo last move
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    while True:
      color, where = H.pop()
      if color > 0: # normal move, erase it
        brd[where] = EMPTY
        return
      else: # capture move, restore it
        brd[where] = -color

def interact(use_tt):
  p = Position(2,2)
  move_record = []  # used for undo, only need locations
  positions = [p.brdstring()] # used for positional superko
  move_made = False
  while True:
    showboard(p)
    for x in positions: print(x)
    print('move_record', move_record)
    print('tromp-taylor score (black, white)',p.tromp_taylor_score(),'\n')
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      undo(move_record, p.brd)
      if len(positions)>1: positions.pop()
    elif (cmd[0][0] in POINT_CHARS):
      sofar = p.requestmove(cmd, move_record)
      if sofar: # no liberty violation, check superko
        pstring = p.brdstring()
        if pstring in positions:
          print('superko violation, move not allowed')
          undo(move_record, p.brd)
        else:
          positions.append(pstring)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)
