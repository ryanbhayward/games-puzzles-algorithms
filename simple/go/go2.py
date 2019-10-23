"""
simple Go program  RBH 2019    
  * generate legal moves and game score
  * based on a subset of M Mueller's Go0 Go1 programs
  * also allow rectangular boards, so with columns != rows
             1 <= R <= 9 rows 
             1 <= C <= 9 columns
working features
  * make legal moves (Tromp-Taylor, no suicide, positional superko)
  * show Tromp-Taylor score
TODO
  * code reorg: clean up the parsing (eg do all legal move
    checks without touching history?)
  * also allow suicide? (Tromp-Taylor, allow suicide, positional superko)
"""

import numpy as np
import copy

"""
points on the board
"""

EMPTY, BLACK, WHITE, BORDER, PTS = 0, 1, 2, 3, '.xo#'

def opponent(color): return BLACK + WHITE - color

"""
the board: a one-dimensional string

index psns for a 2x3 board 3 4 5       <- row 1
                           0 1 2       <- row 0
                          
                           0 1 2       <- columns
"""

def coord_to_point(r, c, C): return c + r*C
def point_to_coord(p, C): return divmod(p, C)

def point_to_alphanum(p,C):
  r, c = divmod(p, C+1)
  return 'abcdefghj'[c-1] + '1234566789'[r-1]


class Position: # go board with x,o,e point values
  def __init__(self, row, col):
    self.R, self.C, self.n = row, col, row*col
    self.brd = PTS[EMPTY]*self.n
    self.nbrs = []
    for r in range(row):
      for c in range(col):
        nbs = []
        if r>0:     nbs.append(coord_to_point(r-1,c,C))
        if r<row-1: nbs.append(coord_to_point(r+1,c,C))
        if c>0:     nbs.append(coord_to_point(r,c-1,C))
        if c<col-1: nbs.append(coord_to_point(r,c+1,C))
        self.nbrs.append(nbs)
    for j in range(self.nbrs):
      print(j, self.nbrs[j])

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

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = POINT_CHARS.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def printmenu():
  print('  h             help menu')
  print('  x b2         play x b 2')
  print('  o e3         play o e 3')
  print('  . a2          erase a 2')
  print('  t        toggle: use TT')
  print('  ?           solve state')
  print('  g x/o           genmove')
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

def undo(H, S, p, also_set):  # pop last meta-move
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    st = p.psn_to_str()
    if also_set:
      S.remove(st)
    while True:
      color, where = H.pop()
      print(color, where)
      if color > 0: # normal move, erase it
        print(H,'remove')
        print(p.brd)
        p.brd[where] = EMPTY
        print(p.brd)
        return
      else: # capture move, restore it
        print(H,'restore')
        p.brd[where] = -color

def interact(use_tt):
  p = Position(1,4)
  print(p.R, p.C, p.n, p.fat_n, coord_to_point(0,0,p.C), coord_to_point(p.R-1,p.C-1,p.C))
  p_str = p.psn_to_str()
  print(p_str)
  all_psns = set()
  all_psns.add(p_str)
  history = []  # used for erasing, so only need locations
  while True:
    showboard(p)
    for x in all_psns: 
      print(x)
    print('tromp-taylor score (black, white)',p.tromp_taylor_score(),'\n')
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      undo(history, all_psns, p, True)
    elif (cmd[0][0] in POINT_CHARS):
      if p.requestmove(cmd, history):
        p_str = p.psn_to_str()
        if p_str in all_psns:
          print('superko violation: undoing move')
          undo(history, all_psns, p, True)
        else:
          all_psns.add(p_str)

interact(False)
