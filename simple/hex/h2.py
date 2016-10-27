# hex player              RBH 2016
# style influenced by 
#   * Michi (by Petr Baudis)
#   * Morat (by Timo Ewalds)
#   * Miaowy (by RBH)
#   * Benzene (by 
#       Broderick Arneson, Philip Henderson, Jakub Pawlewicz,
#       Aja Huang, Yngvi Bjornsson, Michael Johanson, Morgan Kan,
#       Kenny Young, Noah Weninger, RBH)
# boardsize constraint: 
#    fat board should fit in dtype uint8
#    for larger boards, increase parent dtype to uint16

import numpy as np
from copy import deepcopy

class Cell: #############  cells #########################
  e,b,w,ch = 0,1,2, '.*@'       # empty, black, white

  def opponent(c): 
    return 3-c

class B: ################ the board #######################

  ### i-o variables
  letters = 'abcdefghijklmnopqrstuvwxyz'
  esc       = '\033['            ###### these are for colors
  endcolor  =  esc + '0m'
  textcolor =  esc + '0;37m'
  color_of  = (textcolor, esc + '0;35m', esc + '0;32m')

  def __init__(self,rows,cols):
    B.r  = rows  
    B.c  = cols
    B.n  = rows*cols   # number cells
    B.g  = 1   # number guard layers that encircle true board
    B.w  = self.c + self.g + self.g  # width of layered board
    B.fat_n = self.w * (self.r + self.g + self.g) # fat-board cells

    B.border = (  # on fat board, location of cell on these borders:
      fat_psn_of(-1,  0),   # black top 
      fat_psn_of(B.r, 0),   # black btm 
      fat_psn_of(0, -1),    # white left
      fat_psn_of(0, B.c) )  # white right
    B.parent = np.array([0]*B.fat_n, dtype=np.uint8)

  # 2x3 board  layers: g==1    g==2      
  #                           *******
  #            *****           *******
  #    ...      o...o           oo...oo
  #     ...      o...o           oo...oo
  #               *****           *******
  #                                *******
      
    B.empty_brd = np.array([0]*self.n, dtype=np.uint8)
    B.empty_fat_brd = np.array(
      ([Cell.b]*self.w) * self.g +
      ([Cell.w]*self.g + [0]*self.c + [Cell.w]*self.g) * self.r +
      ([Cell.b]*self.w) * self.g, dtype=np.uint8)

  # 2x3 board      r,c          positions
  
  #    ...      0 0  0 1  0 2     0  1  2
  #     ...      1 0  1 1  1 2     3  4  5
  
  # 2x3 fat board     r,c                 positions
  
  #  -***-     -1-1 -1 0 -1 1 -1 2 -1 3    0  1  2  3  4
  #   o...o     0-1   0 0  0 1  0 2  0 3    5  6  7  8  9
  #    o...o     1-1   1 0  1 1  1 2  1 3   10 11 12 13 14
  #     -***-     2-1   2 0  2 1  2 2  2 3   15 16 17 18 19
  
### board i-o ##############
def disp(brd): 
  if len(brd)==B.n:  # true board: add outer layers
    s = 2*' ' + ' '.join(B.letters[0:B.c]) + '\n'
    for j in range(B.r):
      s += j*' ' + '{:2d}'.format(j+1) + ' ' + \
        ' '.join([Cell.ch[brd[k + j*B.c]] for k in \
        range(B.c)]) + ' ' + Cell.ch[Cell.w] + '\n'
    return s + (3+B.r)*' ' + ' '.join(Cell.ch[Cell.b]*B.c) + '\n'
  elif len(brd)==B.fat_n: # fat board: just return cells
    s = ''
    for j in range(B.r + B.g + B.g):
      s += (j+1)*' ' + ' '.join([Cell.ch[brd[k + j*B.w]] \
        for k in range(B.w)]) + '\n'
    return s
  else: assert(False)
     
#    powers_of_3 = [1]
    #for j in range(self.n-1): 
      #powers_of_3.append(powers_of_3[j])
    #self.powers_of_3 = np.array(powers_of_3)

#  def brd_to_int(self,brd):
#    return sum(brd*self.powers_of_3) # numpy multiplies vectors componentwise

def psn_of(x,y):
  return x*B.c + y

def fat_psn_of(x,y):
  return (x+ B.g)*B.w + y + B.g

def rc_of(p): # return usual row, col coordinates
  return divmod(p, B.c)

def rc_of_fat(p):  # return usual row, col coordinates
  x,y = divmod(p, B.w)
  return x - B.g, y - B.g

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

def show_board(brd):
  print('\n', paint(disp(brd)))

### connectivity ################################
###   win_check after each move, so using union-find

class UF:        # union find

  def union(x,y,parent):  
    parent[x] = y

  def find(x,P): # using grandparent compression
    px = parent[x]
    if x == px: return x
    gx = parent[px]
    while px != gx:
      parent[x] = gx
      x, px, gx = px, gx, parent[gx]
    return px

### user i-o

def tst(r,c):
  B(r,c)
  print(disp(B.empty_brd))
  print(paint(disp(B.empty_brd)))
  print(disp(B.empty_fat_brd))
  print(paint(disp(B.empty_fat_brd)))

  for r in range(B.r):
    for c in range(B.c):
      p = psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == rc_of(p)
    print('')

  for r in range(-B.g, B.r + B.g):
    for c in range(-B.g, B.c + B.g):
      p = fat_psn_of(r,c)
      #print(r,c,p,B.rc_of_fat(p))
      print('{:3}'.format(p), end='')
      assert (r,c) == (rc_of_fat(p))
    print('')

  f, (a,b,c,d) = B.empty_fat_brd, B.border
  assert(f[a] == Cell.b and f[b] == Cell.b)
  assert(f[c] == Cell.w and f[d] == Cell.w)
  print(B.r, B.c, 'borders',a,b,c,d)

def big_tst():
  for j in range(1,12):
    for k in range(1,12):
      tst(j,k)

## consider all possible isomorphic positions, return min
#def min_iso(L): # using numpy array indexing here
  #return min([brd_to_int( L[Isos[j]] ) for j in range(8)])

# convert from integer for board position
#def base_3( y ): 
#  assert(y <= ttt_states)
#  L = [0]*Cell.n
#  for j in range(Cell.n):
#    y, L[j] = divmod(y,3)
#    if y==0: break
#  return np.array( L, dtype = np.int16)

# input-output ################################################
def char_to_cell(c): 
  return Cell.ch.index(c)

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = Cell.ch.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def printmenu():
  print('  * b2         play * b 2')
  print('  @ e3         play @ e 3')
  print('  u                  undo')
  print('  ?           solve state')
  print('  g */@           genmove')
  print('  t      use trans. table')
  print('  [return]           quit')

def putstone(brd, p, cell):
  brd[p] = cell

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    p = H.pop()
    brd[p] = Cell.e

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    lcn = H.pop()
    brd[lcn] = Cell.e

def printmenu():
  print('  b b2         play b b 2')
  print('  w e3         play w e 3')
  print('  . a2          erase a 2')
  print('  u                  undo')
  print('  ?           solve state')
  print('  g b/w           genmove')
  print('  t      use trans. table')
  print('  [return]           quit')

def make_move(brd, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ndx = Cell.ch.find(cmd[0][0])
      if ndx >= 0:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < B.r and y>=0 and y < B.c:
            p = psn_of(x,y)
            if brd[p] != Cell.e:
              print('\n cell already occupied\n')
              return
            else:   
              putstone(brd, p, ndx)
              H.append(p) # add location to history
              return
          else: 
            print('\n  coordinate off board\n')
            return
    print('\n  make_move did not parse \n')

def interact(use_tt):
  #AB = ({}, {})  # x- and o- dictionaries of alphabeta values
  B(3,3)
  board = deepcopy(B.empty_brd)
  history = []  # used for erasing, so only need locations
  while True:
    show_board(board)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='?':
      print('  coming soon')
      #info(p, use_tt, AB)
    elif cmd[0][0]=='u':
      undo(history, board)
    elif cmd[0][0]=='g':
      print('  coming soon')
      #p.genmove(genmoverequest(cmd), use_tt, AB)
    elif cmd[0][0]=='t':
      use_tt = True
    elif (cmd[0][0] in Cell.ch):
      make_move(board, cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

big_tst()
interact(False)
