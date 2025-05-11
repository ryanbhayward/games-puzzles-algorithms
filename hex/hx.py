"""
  rbh 2025
  based on hexgo.py   
  to be used by hex mmx solver versions
    for a bit of data for Xinyue's thesis :)
"""

import copy
from string import ascii_lowercase

""" 
globals
"""

ROWS, COLS = 3, 3  # board size

N = ROWS * COLS

BLK, WHT, EMP, IO_CH = 0, 1, 2, 'xo.'
BCH, WCH, ECH = IO_CH[BLK], IO_CH[WHT], IO_CH[EMP]

"""
point indices 0 1 2       <- row 0
               3 4 5       <- row 1
                6 7 8       <- row 2
"""

def color_cell(psn, where, color):
  return psn[:where] + color + psn[where+1:]

def rc_to_point(row, col, num_cols):
  return col + row * num_cols

def point_to_rc(p, C): return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_rc(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

NBRS = []
for r in range(ROWS):
  for c in range(COLS):
    nbs = []
    if r > 0:                nbs.append(rc_to_point(r-1, c,   COLS))
    if r > 0 and c < COLS-1: nbs.append(rc_to_point(r-1, c+1, COLS))
    if c > 0:                nbs.append(rc_to_point(r,   c-1, COLS))
    if c < COLS-1:           nbs.append(rc_to_point(r,   c+1, COLS))
    if r < ROWS-1 and c > 0: nbs.append(rc_to_point(r+1, c-1, COLS))
    if r < ROWS-1:           nbs.append(rc_to_point(r+1, c, COLS))
    NBRS.append(nbs)
#print('nbrs', NBRS)

LFT_COL, RGT_COL, TOP_ROW, BTM_ROW = set(), set(), set(), set()
for r in range(ROWS):
  LFT_COL.add(rc_to_point(r, 0, COLS))
  RGT_COL.add(rc_to_point(r, COLS-1, COLS))
for c in range(COLS):
  TOP_ROW.add(rc_to_point(0, c, COLS))
  BTM_ROW.add(rc_to_point(ROWS-1, c, COLS))
#print(LFT_COL, RGT_COL, TOP_ROW, BTM_ROW)

"""
cell order determines move order
"""

CELLS = range(N)  # this order terrible for solving
#if ROWS == 3 and COLS == 3: CELLS = (4,2,6,3,5,1,7,0,8)
#if ROWS == 3 and COLS == 4: CELLS = (0,1,2,3,4,5,6,7,8,9,10,11)
#if ROWS == 3 and COLS == 4: CELLS = (5,6,4,7,2,9,3,8,1,10,0,11)
#if ROWS == 3 and COLS == 4: CELLS = (5,9,10,3,8,1,4,6,2,7,0,11)
#if ROWS == 4 and COLS == 3: CELLS = (4,7,5,6,3,2,8,9,1,10,0,11)
#if ROWS == 4 and COLS == 4: CELLS = (6,9,3,12,2,13,5,10,8,7,1,14,4,11,0,15)

class Cell: ############## board cells ###############

  def from_ch(ch): return IO_CH.index(ch)

  def opponent(c): return 1 - c

  def oppCH(ch): 
    if ch == BCH: return WCH
    return BCH

  def test():
    print('tests for class Cell')
    for ch in IO_CH:
      c = Cell.from_ch(ch)
      outstr = ch + ' ' + str(c) + ' ' + IO_CH[c]
      print(Color.paint(outstr, IO_CH))
    print()
    print('opponent test')
    for j in range(2):
      print(j, Cell.opponent(j))

class Color: ############ for color output ############
  green   = '\033[0;32m'
  magenta = '\033[0;35m'
  grey    = '\033[0;37m'
  end     = '\033[0m'

  def paint(s, chrs):
    p = ''
    for c in s:
      if c == chrs[0]: p += Color.magenta + c + Color.end
      elif c == chrs[1]: p += Color.green + c + Color.end
      elif c.isalpha(): p+= Color.magenta + c + Color.end
      elif c.isnumeric(): p+= Color.green + c + Color.end
      elif c.isprintable(): p += Color.grey + c + Color.end
      else: p += c
    return p

class IO:  ############## hex output #############

  def spread(s): # embed blanks in string
    return ''.join([' ' + c for c in s])
  
  def point_ch(brd, p):
    return brd[p]

  def show_dict(msg, d):
    print('\n' + msg)
    for x in d: print(x, d[x])

  def showboard(brd, r, c): 
    s = '\n'
    s += '  ' + IO.spread(ascii_lowercase[:c]) + '\n'
    for y in range(r):
      s += y*' ' + f'{y+1:2} ' +IO.spread(brd[y*c:(y+1)*c])
      s += ' ' + WCH + '\n'
    s += '   ' + ' '*r + (' ' + BCH)*c
    print(Color.paint(s, IO_CH))

class Position: # hex board 
  def __init__(self, rows, cols):
    self.R, self.C, self.n = rows, cols, rows*cols
    self.brd = ECH*self.n

  def requestmove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd) != 2:
      print('invalid command')
      return ''
    ch = cmd[0][0]
    if ch not in IO_CH:
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
    where = rc_to_point(x,y,self.C)
    if self.brd[where] != ECH:
      print('\n  sorry, position occupied')
      return ''
    return color_cell(self.brd, where, ch)

class Game: #
  def printmenu():
    print('  h                help menu')
    print('  x b2            play x b 2')
    print('  o e3            play o e 3')
    print('  ? x       solve: x to play')
    print('  . a2             erase a 2')
    print('  u                     undo')
    print('  [return]              quit')

  def undo(H, brd):  # pop last move
    if len(H)==1:
      print('\n    original position,  nothing to undo\n')
      return brd
    else:
      H.pop()
      return copy.copy(H[len(H)-1])

Cell.test()
