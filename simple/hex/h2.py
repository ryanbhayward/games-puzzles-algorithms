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
from random import shuffle

class Cell: #############  cells #########################
  e,b,w,ch = 0,1,2, '.*@'       # empty, black, white

  def opponent(c): 
    return 3-c

class B: ################ the board #######################

  # 2x3 naked  1 guard layer   2 " "

  #                           *******
  #            *****           *******
  #    ...      o...o           oo...oo
  #     ...      o...o           oo...oo
  #               *****           *******
  #                                *******

  # naked        row col       positions
  
  #    ...      0 0  0 1  0 2     0  1  2
  #     ...      1 0  1 1  1 2     3  4  5
  
  # fat           row col                 positions
  
  #  -***-     -1-1 -1 0 -1 1 -1 2 -1 3    0  1  2  3  4
  #   o...o     0-1   0 0  0 1  0 2  0 3    5  6  7  8  9
  #    o...o     1-1   1 0  1 1  1 2  1 3   10 11 12 13 14
  #     -***-     2-1   2 0  2 1  2 2  2 3   15 16 17 18 19

  def __init__(self,rows,cols):
    B.r  = rows  
    B.c  = cols
    B.n  = rows*cols   # number cells
    B.g  = 1   # number guard layers that encircle true board
    B.w  = B.c + B.g + B.g  # width of layered board
    B.h  = B.r + B.g + B.g
    B.fat_n = B.h * B.w # fat-board cells

    B.nbr_offset = (-B.w, -B.w+1, 1, B.w, B.w-1, -1)
    #   0 1
    #  5 . 2
    #   4 3

    B.border = (  # on fat board, location of cell on these borders:
      0,                    # top 
      B.fat_n - 1,          # btm 
      B.g*B.w,              # white left
      (1+B.g)*B.w - 1)

    B.empty_brd = np.array([0]*self.n, dtype=np.uint8)
    B.empty_fat_brd = np.array(
      ([Cell.b]*self.w) * self.g +
      ([Cell.w]*self.g + [0]*self.c + [Cell.w]*self.g) * self.r +
      ([Cell.b]*self.w) * self.g, dtype=np.uint8)

    # parent: for union find   is_root(x): return parent[x] == x
    B.parent = np.array([0]*B.fat_n, dtype=np.uint8)
    p = 0
    for fr in range(B.h):
      for fc in range(B.w):
        if fr < B.g:         B.parent[p] = B.border[0] # top
        elif fr >= B.g + B.r: B.parent[p] = B.border[1] # btm
        elif fc < B.g:       B.parent[p] = B.border[2] # left
        elif fc >= B.g + B.c: B.parent[p] = B.border[3] # right
        else:                B.parent[p] = p
        p += 1

##### board i-o

  letters = 'abcdefghijklmnopqrstuvwxyz'
  esc       = '\033['            ###### these are for colors
  endcolor  =  esc + '0m'
  textcolor =  esc + '0;37m'
  color_of  = (textcolor, esc + '0;35m', esc + '0;32m')
  
def disp(brd):   # convert board to string picture

  if len(brd)==B.n:  # true board: add outer layers
    s = 2*' ' + ' '.join(B.letters[0:B.c]) + '\n'
    for j in range(B.r):
      s += j*' ' + '{:2d}'.format(j+1) + ' ' + \
        ' '.join([Cell.ch[brd[k + j*B.c]] for k in \
        range(B.c)]) + ' ' + Cell.ch[Cell.w] + '\n'
    return s + (3+B.r)*' ' + ' '.join(Cell.ch[Cell.b]*B.c) + '\n'

  elif len(brd)==B.fat_n: # fat board: just return cells
    s = ''
    for j in range(B.h):
      s += (j+1)*' ' + ' '.join([Cell.ch[brd[k + j*B.w]] \
        for k in range(B.w)]) + '\n'
    return s
  else: assert(False)
     
def show_board(brd):
  print('\n', paint(disp(brd)))

def disp_parent(parent):  # convert parent to string picture
  psn, s = 0, ''
  for fr in range(B.h):
    s += fr*' ' + ' '.join([
    #      ('{:3d}'.format(parent[psn+k]))     \
           ('  *' if parent[psn+k]==psn+k else \
            '{:3d}'.format(parent[psn+k]))     \
           for k in range(B.w)]) + '\n'
    psn += B.w
  return s

def show_parent(P):
  print(disp_parent(P))

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
  return (x+ B.g)*B.w + y + B.g

def rc_of(p): # return usual row, col coordinates
  return divmod(p, B.c)

def rc_of_fat(p):  # return usual row, col coordinates
  x,y = divmod(p, B.w)
  return x - B.g, y - B.g

############# cell vector to single integer ###########

#    powers_of_3 = [1]
    #for j in range(self.n-1): 
      #powers_of_3.append(powers_of_3[j])
    #self.powers_of_3 = np.array(powers_of_3)

#  def brd_to_int(self,brd):
#    return sum(brd*self.powers_of_3) # numpy multiplies vectors componentwise

### connectivity ################################
###   want win_check after each move, so union find

class UF:        # union find

  def union(parent,x,y):  
    parent[x] = y
    return y

  def find(parent,x): # using grandparent compression
    while True:
      px = parent[x]
      if x == px: return x
      gx = parent[px]
      if px == gx: return px
      parent[x], x = gx, gx

def win_check(P, color):
  if color == Cell.b:
    return UF.find(P, B.border[0]) == UF.find(P, B.border[1])
  return UF.find(P, B.border[2]) == UF.find(P, B.border[3])
      
### user i-o

def tst(r,c):
  B(r,c)
  print(disp(B.empty_brd))
  print(paint(disp(B.empty_brd)))
  print(disp(B.empty_fat_brd))
  print(paint(disp(B.empty_fat_brd)))
  print(disp_parent(B.parent))

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
  for j in range(1,6):
    for k in range(1,10):
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
#def char_to_cell(c): 
#  return Cell.ch.index(c)

def genmoverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid genmove request\n')
  if len(cmd)==2:
    x = Cell.ch.find(cmd[1][0])
    if x == 1 or x == 2:
      return True, cmd[1][0], ''
  return invalid

def empty_cells(brd):
  L = []
  for j in range(B.fat_n):
    if brd[j] == Cell.e: 
      L.append(j)
  return L

def flat_mc_move(brd, P, color):
# coming soon
  pass
  #for c in shuffle(empty_cells(brd)):
  
    

def parent_update(brd, P, psn, color):
# update parent-structure after move color --> psn
  captain = UF.find(P, psn)
  for j in range(6):  # 6 neighbours
    nbr = psn + B.nbr_offset[j]
    if color == brd[nbr]:
      nbr_root = UF.find(P, nbr)
      captain = UF.union(P, captain, nbr_root)

def putstone(brd, p, cell):
  brd[p] = cell

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    nothing to undo\n')
  else:
    lcn = H.pop()
    brd[lcn] = Cell.e

def make_move(brd, P, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      color = Cell.ch.find(cmd[0][0])
      if color >= 0:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < B.r and y>=0 and y < B.c:
            psn = fat_psn_of(x,y)
            if brd[psn] != Cell.e:
              print('\n cell already occupied\n')
              return
            else:   
              putstone(brd, psn, color)
              parent_update(brd, P, psn, color)
              H.append(psn) # add location to history
              if win_check(P, color): print(' win: game over')
              return
          else: 
            print('\n  coordinate off board\n')
            return
    print('\n  make_move did not parse \n')

def act_on_request(board, P, history):
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

  elif cmd[0][0] =='g':
    return True, '\n  coming soon\n'

  elif (cmd[0][0] in Cell.ch):
    make_move(board, P, cmd, history)
    return True, '\n  make_move\n'

  else:
    return True, '\n  unable to parse request\n'

def interact():
  Board = B(4,4)
  board, history = deepcopy(Board.empty_fat_brd), []
  P = deepcopy(Board.parent)
  while True:
    show_board(board)
    show_parent(P)
    ok, msg = act_on_request(board, P, history)
    print(msg)
    if not ok:
      return

#big_tst()
interact()
