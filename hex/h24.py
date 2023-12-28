# simple hex player based on sets                      rbh 2024  
#   ideas from ...
#     * Michi (by Petr Baudis)
#     * Morat (by Timo Ewalds)
#     * Miaowy (by rbh)
#     * Benzene (by 
#         Broderick Arneson, Philip Henderson, Jakub Pawlewicz,
#         Aja Huang, Yngvi Bjornsson, Michael Johanson, Morgan Kan,
#         Kenny Young, Noah Weninger, Chao Gao, rbh)
#     * hex (by Luke Schultz)
#     * hsearch (by Owen Randall)

from copy import deepcopy
from random import shuffle, choice
import math
from hexio import Cell, IO

class B: ################ the board #######################

  # 2x3 board        row col       positions
  #    ...      0 0  0 1  0 2     0  1  2
  #     ...      1 0  1 1  1 2     3  4  5

  ######## positions <------>   row, column coordinates

  def rc_point(self, row, col):
    return col + row*self.c

  def rc_of(self, p): # return usual row, col coordinates
    return divmod(p, B.c)
  
  def show_point_names(self):  # confirm names look ok
    print('\nnames of points\n')
    for y in range(self.r - 1, -1, -1): #print last row first
      for x in range(self.c):
        print(f'{self.rc_point(y, x):3}', end='')
      print()

  def __init__(self, rows, cols):
    B.r, B.c, B.n  = rows, cols, rows*cols
    B.top, B.btm, B.left, B.right = -4, -3, -2, -1
    B.border = (B.top, B.btm, B.left, B.right)

    B.nbr_offset = (-B.n, -B.n+1, 1, B.n, B.n-1, -1)
    #   0 1
    #  5 . 2
    #   4 3

    ### dictionaries
    B.stones = [set(), set()]  # [black stones, white stones]
    B.nbrs      = {} # point -> set of neighbors
    B.blocks    = {} # point -> block (set of points)
    B.liberties = {} # point -> liberties (set of points)
    # parent: for union find  is_root(x): return parent[x] == x
    B.parent    = {} # point -> parent in block

    B.nbrs[B.top] = set(range(B.c))
    B.nbrs[B.btm] = set(range(B.c*(B.r-1), B.n))
    B.nbrs[B.left] = set([self.rc_point(j,0) for j in range(B.r)])
    B.nbrs[B.right] = set([self.rc_point(j,B.c-1) for j in range(B.r)])
    for point in range(B.n):
       B.nbrs[point]      = set()

    board_points = set(range(self.n))
    for y in range(B.r):
      for x in range(B.c):
        p = self.rc_point(y,x)
        for j in B.nbr_offset:
          nbr = j + self.rc_point(y,x) 
          if nbr in board_points:
            B.nbrs[p].add(nbr)
        
    print('\nneighbors of points\n')
    for p in B.nbrs: print(f'{p:2}', B.nbrs[p])
    self.show_point_names()

    for point in range(B.top, self.n):
       B.blocks[point]    = set()
       B.liberties[point] = set()
       B.parent[point]    = point

    for p in range(B.top, self.n):
      self.liberties[p].update(self.nbrs[p])

    print('\nliberties\n')
    for p in range(self.n):
      print(f'{p:2}', self.liberties[p])

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


### mcts ########################################

def legal_moves(board):
  L = []
  for psn in range(B.n):
    if board[psn] == Cell.e:
      L.append(psn)
  return L

### connectivity ################################

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

def putstone_and_update(brd, P, psn, color):
  putstone(brd, psn, color)
  parent_update(brd, P, psn, color)

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
              #putstone(brd, psn, color)
              #parent_update(brd, P, psn, color)
              putstone_and_update(brd, P, psn, color)
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
    #cmd = cmd.split()
    #if (len(cmd) == 2) and (cmd[1][0] in Cell.ch):
    #  ptm = Cell.get_ptm(cmd[1][0])
    #  psn = mcts(board, P, ptm, 10000, 1)
    #  putstone_and_update(board, P, psn, ptm)
    #  history.append(psn)  # add location to history
    #  if win_check(P, ptm): print(' win: game over')
    #else:
    #  return True, '\n did not give a valid player\n'
    #return True, '\n  gen move with mcts\n'

  elif (cmd[0][0] in Cell.ch):
    make_move(board, P, cmd, history)
    return True, '\n  make_move\n'

  else:
    return True, '\n  unable to parse request\n'

def interact():
  Board = B(4,4)
  #board, history = deepcopy(Board.empty_fat_brd), []
  P = deepcopy(Board.parent)
  while True:
    show_board(board)
    print('legal ', legal_moves(board),'\n')
    show_parent(P)
    #sim_test(board, P, Cell.b, 10000)
    #sim_test(board, P, Cell.w, 10000)
    ok, msg = act_on_request(board, P, history)
    print(msg)
    if not ok:
      return

Board = B(2,3)

IO.disp(B.stones, B.r, B.c)

#big_tst()
#interact()
