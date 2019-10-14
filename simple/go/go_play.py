'''
simple Go program  RBH 2019    
  based on M Mueller's go code, extended to rectangular boards
               1 <= R <= 9 rows 
               1 <= C <= 9 columns
features
* make moves
TODO
* make legal moves (Tromp-Taylor,    no suicide, positional superko)
* make legal moves (Tromp-Taylor, allow suicide, positional superko)
* show Tromp-Taylor score
'''

import numpy as np

EMPTY, BLACK, WHITE, GUARD, POINT_CHARS = 0, 1, 2, 3, '.xo'

def opponent(c): return 3-c

# input-output ################################################
def char_to_cell(c): 
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
  for j in range(psn.R): # rows
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(psn.C): # columns
      pretty += ' ' + paint(POINT_CHARS[psn.brd[rc_to_lcn(j,k,psn.C)]])
    pretty += '\n'
  print(pretty)

##################### board state ########################
'''
add guards: bottom row, top row, and between-each-column
so R x C board requires total (R+2) * (C+1) points,
labelled in row by row from bottom

     3x4 board       point indices

 g  g  g  g  g   20 21 22 23 24
 g  .  .  .  .   15 16 17 18 19
 g  .  .  .  .   10 11 12 13 14
 g  .  .  .  .    5  6  7  8  9
 g  g  g  g  g    0  1  2  3  4
'''

def rc_to_lcn(r, c, C): 
  return (C+1) * (r+1) + c + 1

def lcn_to_alphanum(p,C):
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
    self.brd = np.array([0] * self.fat_n)
    for j in range(c + 1):
      self.brd[j]                = GUARD
      self.brd[j + (r+1)*(c+1)]  = GUARD
    for j in range(r):
      self.brd[r*(c+1)] = GUARD

  def makemove(self, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch in POINT_CHARS:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x<0 or x >= self.R or y<0 or y >= self.C:
            print('\n  sorry, coordinate off board')
          else:
            where = rc_to_lcn(x,y,self.C)
            if self.brd[where] != EMPTY:
              print('\n  sorry, position occupied')
            else:
              self.brd[where] = char_to_cell(ch)
              H.append(where) # add location to history

'''
valid_tromp-taylor_move(where, color):
  brd[where] = color
  capture = False
  for each nbr of where:
    capture = capture_opp_group(nbr)
  if not capture:
    if has_no_liberties(where):
      brd[where] = EMPTY
      return False
  return True
'''

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    lcn = H.pop()
    brd[lcn] = EMPTY

def interact(use_tt):
  p = Position(1,1)
  history = []  # used for erasing, so only need locations
  while True:
    showboard(p)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      undo(history, p.brd)
    elif (cmd[0][0] in POINT_CHARS):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)
