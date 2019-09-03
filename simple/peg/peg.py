# simple peg solitaire
# boardsize constraint: 
#    fat board should fit in dtype uint8
#    for larger boards, increase parent dtype to uint16

import numpy as np
from copy import deepcopy
from random import shuffle, choice
import math

class Cell: #############  cells #########################
  e,p,z,ch = 0,1,2, '.*@'       # empty, peg, offboard

class B: ################ the board #######################

  # 2x3 naked  1 guard layer  

  #             @@@@@        
  #    ...      @...@       
  #    ...      @...@      
  #             @@@@@     
  #                      

  # naked       naked positions    fat positions
  
                 
  #                                 0  1  2  3  4
  #    ...         0 1 2            5  6  7  8  9
  #    ...         3 4 5           10 11 12 13 14
  #                                15 16 17 18 19

  def __init__(self,rows,cols):
    B.r  = rows  
    B.c  = cols
    B.n  = rows*cols   # number cells
    B.w  = B.c + 2  # width of layered board
    B.h  = B.r + 2
    B.fat_n = B.h * B.w # fat-board cells

    B.nbr_offset = (-B.w, -1, 1, B.w)
    #    0
    #  1 . 2
    #    3

    B.empty_brd = np.array([Cell.p]*self.n, dtype=np.uint8)
    B.empty_fat_brd = np.array([Cell.p]*self.fat_n, dtype=np.uint8)
    for j in range(B.w): 
      B.empty_fat_brd[j] = Cell.z
      B.empty_fat_brd[ j + (B.h-1)*B.w ] = Cell.z
    for k in range(B.h): 
      B.empty_fat_brd[k*B.w] = Cell.z
      B.empty_fat_brd[(k+1)*B.w-1] = Cell.z

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

######## positions <------>   row, column coordinates

def psn_of(x,y):
  return x*B.c + y

def fat_psn_of(x,y):
  return (x+ 1)*B.w + y + 1

def rc_of(p): # return usual row, col coordinates
  return divmod(p, B.c)

def rc_of_fat(p):  # return usual row, col coordinates
  x,y = divmod(p, B.w)
  return x - 1, y - 1

### mcts ########################################

#def legal_moves(board):
  #L = []
  #for psn in range(B.fat_n):
    #if board[psn] == Cell.e:
      #L.append(psn)
  #return L

### user i-o

def tst(r,c):
  B(r,c)
  #print(disp(B.empty_fat_brd))
  print(paint(disp(B.empty_fat_brd)))

  for r in range(B.r):
    for c in range(B.c):
      p = psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == rc_of(p)
    print('')

  for r in range(-1, B.r + 1):
    for c in range(-1, B.c + 1):
      p = fat_psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == (rc_of_fat(p))
    print('')

def big_tst():
  for j in range(1,6):
    for k in range(1,10):
      tst(j,k)

# input-output ################################################
#def char_to_cell(c): 
#  return Cell.ch.index(c)

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

def putstone(brd, k, cell):
  brd[k] = cell

#def putstone_and_update(brd, P, psn, color):
  #putstone(brd, psn, color)
  #parent_update(brd, P, psn, color)

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
#
 # elif cmd[0][0] =='g':
 #   cmd = cmd.split()
 #   if (len(cmd) == 2) and (cmd[1][0] in Cell.ch):
 #     #putstone_and_update(board, P, psn, ptm)
 #     # history.append(psn)  # add location to history
 #     if win_check(P, ptm): print(' win: game over')
 #   else:
 #     return True, '\n did not give a valid player\n'
 #  return True, '\n  gen move with mcts\n'

  else:
    return True, '\n  unable to parse request\n'

def interact():
  Board = B(4,4)
  board, history = deepcopy(Board.empty_fat_brd), []
  while True:
    show_board(board)
    #print('legal ', legal_moves(board),'\n')
    ok, msg = act_on_request(board, history)
    print(msg)
    if not ok:
      return

big_tst()
#tst(3,4)
interact()
