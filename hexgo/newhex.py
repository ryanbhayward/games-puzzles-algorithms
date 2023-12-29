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

#from copy import deepcopy
#from random import shuffle, choice
#import math
from time import time
from hexgo import Cell, Color, Game, IO, Pt, UF

class B: ################ the board #######################
  #   2x3 board      row,col            positions
  #   * * * * *                     0   1   2   3   4
  #    @ . . . @    0,0  0,1  0,2     5   6   7   8   9
  #     @ . . . @     1,0  1,1  1,2    10  11  12  13  14  
  #      * * * * *                       15  16  17  18  19

  def show_all(self):
    bs = IO.board_str(self.stones, self.n)
    IO.disp(self.game_type, bs, self.r, self.c)
    Pt.show_point_names(self.game_type, self.r, self.c)
    IO.show_blocks(self.n, self.stones, self.parents, self.blocks, self.liberties)

  def __init__(self, rows, cols):
    B.game_type = Game.hex_game
    B.r, B.c, B.fat_r, B.fat_c = rows, cols, rows+2, cols+2
    B.n, B.fat_n = B.r*B.c, B.fat_r*B.fat_c 
    B.top, B.btm, B.lft, B.rgt =  1, B.fat_n-2, B.fat_c, B.fat_n-B.fat_c-1
    B.border = (B.top, B.btm, B.lft, B.rgt)

    B.nbr_offset = (-B.fat_c, -B.fat_c+1, 1, B.fat_c, B.fat_c-1, -1)
    #   0 1
    #  5 . 2
    #   4 3

    ### dictionaries
    B.stones = [set(), set()]  # [black stones, white stones]
    B.nbrs      = {} # point -> neighbor set
    B.blocks    = {} # point -> block set 
    B.liberties = {} # point -> liberties set
    # parents: for union find  is_root(x): return parents[x] == x
    B.parents    = {} # point -> parents in block

    B.nbrs[B.top] = set(range(B.c))
    B.nbrs[B.btm] = set(range(B.c*(B.r-1), B.n))
    B.nbrs[B.lft] = set([Pt.rc_point(j, 0, B.c) for j in range(B.r)])
    B.nbrs[B.rgt] = set([Pt.rc_point(j, B.c-1, B.c) for j in range(B.r)])
    for point in range(B.n): B.nbrs[point] = set()

    board_points = set(range(self.n))
    for y in range(B.r):
      for x in range(B.c):
        p = Pt.rc_point(y, x, B.c)
        for j in B.nbr_offset:
          nbr = j + Pt.rc_point(y, x, B.c) 
          if nbr in board_points:
            B.nbrs[p].add(nbr)

    IO.show_dict('hex neighbors', B.nbrs)

    for point in range(B.top, self.n):
       B.blocks[point]    = set()
       B.liberties[point] = set()
       B.parents[point]    = point

    for p in range(B.top, self.n):
      self.liberties[p].update(self.nbrs[p])

def disp_parents(parents):  # convert parents to string picture
  psn, s = 0, ''
  for fr in range(B.h):
    s += fr*' ' + ' '.join([
    #      ('{:3d}'.format(parents[psn+k]))     \
           ('  *' if parents[psn+k]==psn+k else \
            '{:3d}'.format(parents[psn+k]))     \
           for k in range(B.w)]) + '\n'
    psn += B.w
  return s

def show_parents(P):
  print(disp_parents(P))

### mcts ########################################

def legal_moves(board):
  L = []
  for psn in range(B.n):
    if board[psn] == Cell.e:
      L.append(psn)
  return L

### connectivity ################################

class UF:        # union find

  def union(parents,x,y):  
    parents[x] = y
    return y

  def find(parents,x): # using grandparents compression
    while True:
      px = parents[x]
      if x == px: return x
      gx = parents[px]
      if px == gx: return px
      parents[x], x = gx, gx

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
  print(disp_parents(B.parents))

  for r in range(B.r):
    for c in range(B.c):
      p = psn_of(r,c)
      print('{:3}'.format(p), end='')
      assert (r,c) == IO.rc_of(p)
    print('')

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

def parents_update(brd, P, psn, color):
# update parents-structure after move color --> psn
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
  parents_update(brd, P, psn, color)

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
              #parents_update(brd, P, psn, color)
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
  P = deepcopy(Board.parents)
  while True:
    show_board(board)
    print('legal ', legal_moves(board),'\n')
    show_parents(P)
    #sim_test(board, P, Cell.b, 10000)
    #sim_test(board, P, Cell.w, 10000)
    ok, msg = act_on_request(board, P, history)
    print(msg)
    if not ok:
      return

start_time = time()
board = B(6,6)
board.show_all()
end_time = time()
print('time ', end_time - start_time)

#big_tst()
#interact()
