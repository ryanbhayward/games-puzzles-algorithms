# simple peg solitaire
# boardsize constraint: 
#    fat board should fit in dtype uint8
#    for larger boards, increase parent dtype to uint16

import numpy as np
from copy import deepcopy
from random import shuffle, choice
#import math

class Cell: #############  cells #########################
  h,p,g,ch = 0,1,2, '.*@'       # hole, peg, guard (offboard)

class B: ################ the board #######################

  # 2x3 naked  2 guard layers
  #            @@@@@@@
  #            @@@@@@@
  #    ...     @@...@@
  #    ...     @@...@@
  #            @@@@@@@
  #            @@@@@@@

  # naked       naked positions    fat positions
  #                                 0  1  2  3  4  5  6
  #                                 7  8  9 10 11 12 13
  #    ...         0 1 2           14 15 16 17 18 19 20
  #    ...         3 4 5           21 22 23 24 25 26 27
  #                                28 29 30 31 32 33 34

  def __init__(self, rows, cols):
    B.r, B.c  = rows, cols
    B.n       = rows*cols        # number cells
    B.w, B.h  = B.c + 4, B.r + 4 # width, height of padded board
    B.fat_n   = B.h * B.w        # number fat-board cells

    B.offsets = (-1, -B.w, B.w, 1)  #neighbour offsets
    #    1
    #  0 . 3
    #    2

    B.fat_brd = np.array([Cell.p]*self.fat_n, dtype=np.uint8)
    
    for j in range(B.w*2):        # guard top, bottom: 2 rows each
      guardify(B.fat_brd,j)
      guardify(B.fat_brd,B.fat_n-(j+1))
    for k in range(B.r):          # guard left, right: 2 cols each
      guardify(B.fat_brd, fat_psn_of(k,-2))
      guardify(B.fat_brd, fat_psn_of(k,-1))
      guardify(B.fat_brd, fat_psn_of(k,B.c))
      guardify(B.fat_brd, fat_psn_of(k,B.c+1))

##### board i-o

  letters = 'abcdefghijklmnopqrstuvwxyz'
  esc       = '\033['            ###### these are for colors
  endcolor  =  esc + '0m'
  textcolor =  esc + '0;37m'
  color_of  = (textcolor, esc + '0;35m', esc + '0;32m')
  
def disp(brd):   # fat board: just return cells
  assert(len(brd)==B.fat_n) 
  s = ''
  for j in range(B.h):
    s += ' '.join([Cell.ch[brd[k + j*B.w]] \
      for k in range(B.w)]) + '\n'
  return s

def show_board(brd):
  print('')
  print(paint(disp(brd)))

############ cell operations #######################

def guardify(brd, p):   # mark cell as permanently off-board
  brd[p] = Cell.g
     
def change_cell(brd, p): # change unguarded cell, hole <-> peg
  bp = brd[p]
  if bp != Cell.g:
    brd[p] = opposite(brd[p])
     
############ colored output ######################

def paint(s):  # replace with colored characters
  p = ''
  for c in s:
    x = Cell.ch.find(c)
    if x >= 0:
      p += B.color_of[x] + c + B.endcolor
    elif c.isalnum():
      p += B.textcolor + c + B.endcolor
    else: p += c
  return p

######## positions <--> row, column coordinates

def psn_of(x,y):
  return x*B.c + y

def fat_psn_of(x,y):
  return (x+2)*B.w + y + 2

def fat_w(r,c):  # fat board width
  return c+4

def rc_of(p): # return usual row, col coordinates
  return divmod(p, B.c)

def rc_of_fat(p):  # return usual row, col coordinates
  x,y = divmod(p, B.w)
  return x - 2, y - 2

def can_jump(brd, psn, delta):
  return ((brd[psn + delta] == Cell.p) and 
          (brd[psn + delta + delta] == Cell.h))

def legal_moves(brd, r, c):
  L = []
  for j in range(r):
    for k in range(c):
       psn = fat_psn_of(j, k)
       if brd[psn] == Cell.p:  # peg
         # try ....  left,       up,       down,      right
         for delta in (-1,   -fat_w(r,c), fat_w(r,c),     1):  
           if can_jump( brd, psn, delta ):
             L.append( (psn, delta) )
  return L

### user i-o

def tst(r,c):
  B(r,c)
  #print(disp(B.fat_brd))
  print(paint(disp(B.fat_brd)))

  for r in range(B.r):
    for c in range(B.c):
      p = psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == rc_of(p)
    print('')

  for r in range(-2, B.r + 2):
    for c in range(-2, B.c + 2):
      p = fat_psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == (rc_of_fat(p))
    print('')

def big_tst():
  for j in range(1,6):
    for k in range(1,10):
      tst(j,k)

# input-output ################################################

def genmoverequest(cmd):
  #cmd = cmd.split()
  #invalid = (False, None, '\n invalid genmove request\n')
  #if len(cmd)==2:
  #  x = Cell.ch.find(cmd[1][0])
  #  if x == 1 or x == 2:
  #    return True, cmd[1][0], ''
  #return invalid
  return true

def empty_cells(brd):
  L = []
  for j in range(B.fat_n):
    if brd[j] == Cell.e: 
      L.append(j)
  return L

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    nothing to undo\n')
  #else:
  #  lcn = H.pop()
  #  brd[lcn] = Cell.e

def act_on_request(board, history):
  cmd = input(' ')

  if len(cmd) == 0:
    return False, '\n ... adios :)\n'

  elif cmd[0][0] =='h':
    return True, '\n' +\
      ' * b2       play b b 2\n' +\
      ' @ e3       play w e 3\n' +\
      ' g b/w         genmove\n' +\
      ' u                undo\n' +\
      ' [return]         quit\n'

  elif cmd[0][0] =='?':
    return True, '\n  coming soon\n'

  elif cmd[0][0] =='u':
    undo(history, board)
    return True, '\n  undo\n'

  else:
    return True, '\n  unable to parse request\n'

def opposite(c):  #  hole <--> peg
  return 1-c

def peg_move(b, p, d):  # board, position, delta
  bp, p2, p3 = b[p], p + d, p + d + d
  assert(  (bp != Cell.g) and
           (bp == b[p2]) and
           (b[p3] == opposite(bp)) )
  for x in (p, p2, p3):
    change_cell(b, x)
  show_board(b)

def interact():
  Board = B(4,4)
  board, history = deepcopy(Board.fat_brd), []
  while True:
    show_board(board)
    #print('legal ', legal_moves(board),'\n')
    ok, msg = act_on_request(board, history)
    print(msg)
    if not ok:
      return

#big_tst()
#tst(3,4)
#interact()
#Board = B(4,4)
#board = deepcopy(Board.fat_brd)

# more tests
#show_board(board)
#change_cell(board,fat_psn_of(2,2))
#show_board(board)
#change_cell(board,fat_psn_of(2,2))
#guardify(board,fat_psn_of(2,2))
#show_board(board)

Board = B(9,9)
board = deepcopy(Board.fat_brd)
change_cell(board,fat_psn_of(4,4))
for j in range(3):
  for k in range(3):
    guardify(board, fat_psn_of(j,k))
    guardify(board, fat_psn_of(j,k+6))
    guardify(board, fat_psn_of(j+6,k))
    guardify(board, fat_psn_of(j+6,k+6))
show_board(board)

# TODO fix this with proper python loop-break idiom
legal = legal_moves(board, B.r, B.c)
t = 0
while len(legal)>0:
  print(len(legal), ' legal moves here')
  mv = choice(legal)
  peg_move(board, mv[0], mv[1])
  legal = legal_moves(board, B.r, B.c)
  t += 1
  print('         ', t, ' moves so far')
