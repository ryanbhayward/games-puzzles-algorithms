# classic ttt: 3x3 board          RBH 2016
# - genmove finds value of all moves, using alphabeta search
# - implemented this alphabeta improvement:
#  - instead of searching over all children of a node,
#  - search only over non-isomorphic children
#  - (any two isomorphic children will have the same value)
#  - the symmetry group (rotate/flip) of the board has 8 elements:
#  -   if any two symmetries operations yield the same position, then
#  -   the two corresponding positions are isomorphic
# 2019 
#  - added negamax,  740170 nodes from root
# TODO
#  - switch to lines format?
#  - lines format: record impossible-to-complete lines
#  - check for winning move (any linesum 2) before search
#  - check for no-win-possible (all lines impossible-to-complete)
#  - check for forced moves (no win possible: block winning opponent moves)

import numpy as np

class TransposType:
  LOWER = 0;
  EXACT = 1;
  UPPER = 2;

class Transpos:
  type = None
  depth = None
  value = None

  def __init__(self, type, depth, value):
    self.type = type
    self.depth = depth
    self.value = value

class Cell: # each cell is one of these: empty, x, o
  n,e,x,o,chars = 9,0,1,2,'.xo' 

def opponent(c): return 3-c

# each cell is 0,1,2
# so number positions == 3**9
# can represent position as 9-digit base_3 number

ttt_states = 19683  # 3**Cell.n
powers_of_3 = np.array( # for converting position to base_3 int
  [1, 3, 9, 27, 81, 243, 729, 2187, 6561], dtype=np.int16)

def board_to_int(B):
  return sum(B*powers_of_3) # numpy multiplies vectors componentwise

# consider all possible isomorphic positions, return min
def min_iso(L): # using numpy array indexing here
  return min([board_to_int( L[Isos[j]] ) for j in range(8)])

# convert from integer for board position
def base_3( y ): 
  assert(y <= ttt_states)
  L = [0]*Cell.n
  for j in range(Cell.n):
    y, L[j] = divmod(y,3)
    if y==0: break
  return np.array( L, dtype = np.int16)

# input-output ################################################
def char_to_cell(c): 
  return Cell.chars.index(c)

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
    x = Cell.chars.find(cmd[1][0])
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
    x = Cell.chars.find(s[0])
    if x > 0:
      return stonecolors[x] + s + colorend
    elif s.isalnum():
      return textcolor + s + colorend
    return s

  pretty = '\n   ' 
  for c in range(3): # columns
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(3): # rows
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(3): # columns
      pretty += ' ' + paint(Cell.chars[psn.brd[rc_to_lcn(j,k)]])
    pretty += '\n'
  print(pretty)

### permutations showing possible board isomorphisms
Isos = np.array(( (0,1,2,3,4,5,6,7,8),
         (0,3,6,1,4,7,2,5,8),
         (2,1,0,5,4,3,8,7,6),
         (2,5,8,1,4,7,0,3,6),
         (8,7,6,5,4,3,2,1,0),
         (8,5,2,7,4,1,6,3,0),
         (6,7,8,3,4,5,0,1,2),
         (6,3,0,7,4,1,8,5,2)
         ), dtype = np.int8)

Win_lines = np.array(( # 8 winning lines, as location triples
  (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)
  ), dtype=np.int8)

##################### board state ########################
# cell indices, or locations:
#   0 1 2
#   3 4 5
#   6 7 8

def rc_to_lcn(r,c): 
  return r*3 + c

def lcn_to_alphanum(p):
  r, c = divmod(p,3)
  return 'abc'[c] + '123'[r]

class Position: # ttt board with x,o,e cells
  def legal_moves(self):
    L = []
    for j in range(Cell.n):
      if self.brd[j]==Cell.e: 
        L.append(j)
    return L

  def non_iso_moves(self, L, cell): # number of non-isomorphic moves
    assert(len(L)>0)
    H, X = [], []
    for j in range(len(L)):
      p = L[j]
      self.brd[p] = cell
      h = min_iso(self.brd)
      if h not in H:
        H.append(h)
        X.append(j)
      self.brd[p] = Cell.e
    L = np.array(L)
    X = np.array(X)
    return L[X]

  def has_win(self, z):
    win_found = False
    for t in Win_lines:
      if (self.brd[t[0]] == z and
          self.brd[t[1]] == z and
          self.brd[t[2]] == z):
        return True
    return False

  def game_over(self):
    win_found = False
    for z in (Cell.x, Cell.o):
      if (self.has_win(z)):
        print('\n  game_over: ',Cell.chars[z],'wins\n')
        return True
    return False

  def putstone(self, row, col, color):
    self.brd[rc_to_lcn(row,col)] = color

  def __init__(self, y):
    self.brd = base_3(y)

  def genmove(self, request, use_tt, AB):
    if request[0]:
      L = self.legal_moves()
      if len(L)==0:
        print('board full, no move possible')
      else:
        ptm = char_to_cell(request[1])
        if self.has_win(ptm) or self.has_win(opponent(ptm)):
          print('board already has winning line(s)')
        else:
          A = self.non_iso_moves(L,ptm)
          for cell in A:
            self.brd[cell] = ptm
            print(' ',Cell.chars[ptm],'plays',lcn_to_alphanum(cell),end='')
            ab, c = ab_neg(use_tt, AB, 0,0,self,opponent(ptm),-1,1)
            print('  result','{:2d}'.format(-ab), '  nodes',c)
            self.brd[cell] = Cell.e   
    else:
      print(request[2])

  def makemove(self, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch in Cell.chars:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < 3 and y>=0 and y < 3:
            self.putstone(x, y, char_to_cell(ch))
            H.append(rc_to_lcn(x,y)) # add location to history
            return
          else: print('\n  coordinate off board')
    print('  ... ? ... sorry ...\n')

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
  else:
    lcn = H.pop()
    brd[lcn] = Cell.e

####################### alpha-beta negamax search
def ab_neg(use_tt, AB, calls, d, psn, ptm, alpha, beta): # ptm: 1/0/-1 win/draw/loss
  o_alpha = alpha
  if use_tt:
    b_int = board_to_int(psn.brd)
    if b_int in AB[ptm-1] and (AB[ptm-1][b_int].depth >= d):
      t_pos = AB[ptm - 1][b_int]
      if t_pos.type == TransposType.EXACT:
        return t_pos.value, 0
      elif t_pos.type == TransposType.UPPER:
        beta = min(beta, t_pos.value)
      elif t_pos.type == TransposType.LOWER:
        alpha = max(alpha, t_pos.value)
      if alpha >= beta:
        return t_pos.value, 0
  calls += 1
  if psn.has_win(ptm):     
    return 1, calls  # previous move created win
  L = psn.legal_moves()
  if len(L) == 0:          
    return 0, calls  # board full, no winner
  A = psn.non_iso_moves(L,ptm)
  so_far = -1  # best score so far
  for cell in A:
    psn.brd[cell] = ptm
    ab, c = ab_neg(use_tt, AB, 0, d+1, psn, opponent(ptm), -beta, -alpha)
    so_far = max(so_far,-ab)
    calls += c
    psn.brd[cell] = Cell.e   # reset brd to original
    alpha = max(alpha, so_far)
    if alpha >= beta:
      break
  if use_tt:
    if so_far <= o_alpha:
      AB[ptm - 1][b_int] = Transpos(type=TransposType.UPPER,depth=d,value=so_far)
    elif so_far >= o_alpha:
      AB[ptm - 1][b_int] = Transpos(type=TransposType.LOWER, depth=d, value=so_far)
    else:
      AB[ptm - 1][b_int] = Transpos(type=TransposType.EXACT, depth=d, value=so_far)
  return so_far, calls

def negamax(calls, d, psn, ptm): # ptm: 1/0/-1 win/draw/loss
  calls += 1
  progress = calls
  if psn.has_win(ptm):     
    return 1, calls  # previous move created win
  L = psn.legal_moves()
  if len(L) == 0:          
    return 0, calls  # board full, no winner
  so_far = -1  # best score so far
  for cell in L:
    psn.brd[cell] = ptm
    mm, c = negamax(0, d+1, psn, opponent(ptm))
    so_far = max(so_far,-mm)
    calls += c
    psn.brd[cell] = Cell.e   # reset brd to original
  return so_far, calls

def info(p, use_tt, AB):
    h, L = min_iso(p.brd), p.legal_moves()
    print('  min_iso', h, '\n  legal moves', L)
    print('  non-isomorphic moves x o', p.non_iso_moves(L,Cell.x), 
                                        p.non_iso_moves(L,Cell.o))
    for cell in (Cell.x, Cell.o):
      print('  ',Cell.chars[cell], 'alphabeta',end='')
      ab, c = ab_neg(use_tt, AB, 0, 0, p, cell, -1, 1)
      print('  result','{:2d}'.format(ab), '  nodes',c)
      print('  ',Cell.chars[cell], 'negamax',end='')
      s, c = negamax(0, 0, p, cell)
      print('  result','{:2d}'.format(s), '  nodes',c)
    if p.game_over():
      pass

def interact(use_tt):
  AB = ({}, {})  # x- and o- dictionaries of alphabeta values
  p = Position(0)
  history = []  # used for erasing, so only need locations
  while True:
    showboard(p)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='?':
      info(p, use_tt, AB)
    elif cmd[0][0]=='u':
      undo(history, p.brd)
    elif cmd[0][0]=='g':
      p.genmove(genmoverequest(cmd), use_tt, AB)
    elif cmd[0][0]=='t':
      use_tt = not(use_tt)
      if not (use_tt): print('\n not using TT\n')
      else: print('\n using TT\n')
    elif (cmd[0][0] in Cell.chars):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)

