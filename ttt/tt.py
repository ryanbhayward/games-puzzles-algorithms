# classic ttt: 3x3 board  rbh (2016 -- '25)
#      - no numpy
#      - no alphabeta (in previous version of this program)
#      - print non-iso moves
#      - simple negamax (no tt)

#      - exercise 1: early-win-abort improve negamax?
#      - exercise 2: non_iso_moves improve negamax?
#      - exercise 3: opp't win-threats?

# todo? board class with sets

# - genmove: negamax, all moves
# - negamax
#  - search only over non-isomorphic children
#  - board symmetry group (rotate/flip) has 8 elements

from math import factorial

class Cell: # each cell is one of these: empty, x, o
  n, e, x, o, chars  = 9, 0, 1, 2, '.xo'

def opponent(c): return 3 - c

# cells 0,1,2, 3**9 positions, can hash psn as 9-digit base_3 integer
powers_of_3 = (# for conversion from vector to integer
  1, 3, 9, 27, 81, 243, 729, 2187, 6561)

def mynumber(n):
  return n if n>0 else '-'

def board_to_int(B):
  return sum([B[j]*powers_of_3[j] for j in range(Cell.n)]) 

def min_iso(L): # all positions in L are iso: return min board_to_int
  return min([board_to_int([L[Isos[j][k]] for k in range(Cell.n)]) for j in range(8)])

def base_3(y): # int_to_board
  assert(y <= 19683) # 3**Cell.n, also number of ttt positions
  L = [0]*Cell.n
  for j in range(Cell.n):
    y, L[j] = divmod(y,3)
    if y==0: break
  return L

def num_tokens(brd):
  return Cell.n - brd.count(0)

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
  print('  s        toggle: use isomorphisms')
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

### isomorphism permutations
Isos = ( (0,1,2,3,4,5,6,7,8),
         (0,3,6,1,4,7,2,5,8),
         (2,1,0,5,4,3,8,7,6),
         (2,5,8,1,4,7,0,3,6),
         (8,7,6,5,4,3,2,1,0),
         (8,5,2,7,4,1,6,3,0),
         (6,7,8,3,4,5,0,1,2),
         (6,3,0,7,4,1,8,5,2)  )

Win_lines = ( # 8 winning lines, as location triples
  (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6) )

##################### board state ########################
#   cell names   0 1 2
#                3 4 5
#                6 7 8

def rc_to_lcn(r,c): 
  return r*3 + c

def lcn_to_alphanum(p):
  r, c = divmod(p,3)
  return 'abc'[c] + '123'[r]

class Position: # ttt board with x,o,e cells
  def legal_moves(self):
    L = []
    #for j in (4, 0, 2, 6, 8, 1, 3, 5, 7):
    for j in range(Cell.n):
      if self.brd[j]==Cell.e: 
        L.append(j)
    return L

  def non_iso_moves(self, L, cell): # non-isomorphic moves
    assert(len(L)>0)
    H, X = [], []  # hash values, moves
    for j in range(len(L)):
      p = L[j]
      self.brd[p] = cell
      h = min_iso(self.brd)
      if h not in H:
        H.append(h)
        X.append(p)
      self.brd[p] = Cell.e
    return X

  def has_win(self, z):
    for t in Win_lines:
      if (self.brd[t[0]] == z and
          self.brd[t[1]] == z and
          self.brd[t[2]] == z):
         return True
    return False

  def game_over(self):
    for z in (Cell.x, Cell.o):
      if (self.has_win(z)):
        print('\n  game_over: ',Cell.chars[z],'wins\n')
        return True
    return False

  def putstone(self, row, col, color):
    self.brd[rc_to_lcn(row,col)] = color

  def __init__(self, y):
    self.brd = base_3(y)

  def genmove(self, request, use_tt, use_iso, MMX):
    if request[0]:
      L = self.legal_moves()
      if len(L)==0:
        print('board full, no move possible')
      else:
        ptm = char_to_cell(request[1])
        if self.has_win(ptm) or self.has_win(opponent(ptm)):
          print('board already has winning line(s)')
        else:
          for cell in L:
            self.brd[cell] = ptm
            print(' ',Cell.chars[ptm],'plays',lcn_to_alphanum(cell),end='')
            nmx, c = negamax(use_tt, use_iso, MMX, 0, 0, self, opponent(ptm))
            print('  result','{:2d}'.format(-nmx), '  nodes',c)
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

####################### negamax 
def negamax(use_tt, use_iso, MMX, calls, d, psn, ptm): # 1/0/-1 win/draw/loss
  calls += 1
  psn_int = board_to_int(psn.brd)
  if use_tt and (psn_int in MMX[ptm - 1]): 
    return MMX[ptm - 1][psn_int], calls
  if psn.has_win(opponent(ptm)):     
    return -1, calls  # previous move created win
  G = psn.legal_moves()
  if len(G) == 0:          
    return 0, calls  # board full, no winner
  L = psn.non_iso_moves(G, ptm) if use_iso else G
  so_far = -1  # best score so far
  for cell in L:
    psn.brd[cell] = ptm
    nmx, c = negamax(use_tt, use_iso, MMX, 0, d+1, psn, opponent(ptm))
    so_far, calls = max(so_far, -nmx), calls + c
    psn.brd[cell] = Cell.e  # reset brd to original
    #if so_far == 1: break   # improvement: return once win found
  if use_tt: MMX[ptm - 1][psn_int] = so_far
  if d == 0 and use_tt: 
    xsize, osize = len(MMX[0]), len(MMX[1])
    print('\n  TT size', xsize, osize, xsize+osize)
  return so_far, calls

def see_positions(ALL, psn, optm): # see all positions, no win-check
  psn_int = board_to_int(psn.brd)
  if psn_int in ALL[optm - 1]: return 
  else: ALL[optm - 1].add(psn_int)
  G = psn.legal_moves()
  if len(G) == 0: return 
  for cell in G:
    psn.brd[cell] = optm
    see_positions(ALL, psn, opponent(optm))
    psn.brd[cell] = Cell.e  # reset brd to original
  return 

def info(p, use_tt, use_iso, MMX):
    h, L = min_iso(p.brd), p.legal_moves()
    print('  min_iso', h, '\n  legal moves', L)
    print('  non-isomorphic moves x o', p.non_iso_moves(L,Cell.x), 
                                        p.non_iso_moves(L,Cell.o))
    for ptm in (Cell.x, Cell.o):
      print('  ',Cell.chars[ptm], 'minimax',end='')
      nmx, c = negamax(use_tt, use_iso, MMX, 0, 0, p, ptm)
      print('  result','{:2d}'.format(nmx), '  nodes',c)
    if p.game_over():
      pass

def psns_info(ALLPSNS):
  for j in range(1,-1,-1):
    sizes = [0]*(1+Cell.n)
    for k in ALLPSNS[j]:
      sizes[num_tokens(base_3(k))] += 1
    print()
    print(len(ALLPSNS[j]), 'psns with', Cell.chars[opponent(j+1)],'to move')
    print('\noccupied cells   number psns')
    for j in range(1+Cell.n):
      print('   ',j, '              ', mynumber(sizes[j]))

def msg(tt, iso):
  if not tt and not iso: return("no TT, no isomorphisms")
  elif not tt: return("isomorphisms but no TT")
  elif iso: return("isomorphisms and TT")
  else: return("TT but no isomorphisms")

def interact(use_tt, use_iso):
  MMX = ({}, {})  # x and o dictionaries of minimax values
  ALLPSNS = (set(), set())  # x and o dictionaries of 0 values
  print(len(ALLPSNS[Cell.x-1]), len(ALLPSNS[Cell.o-1]))
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
    if cmd[0][0]=='m':
      L = p.legal_moves()
      mx = p.non_iso_moves(L, Cell.x)
      mo = p.non_iso_moves(L, Cell.o)
      print('non-isomorphic x moves', mx)
      print('non-isomorphic o moves', mo)
    elif cmd[0][0]=='#':
      q = Position(0)
      see_positions(ALLPSNS, q, Cell.o)
      psns_info(ALLPSNS)
    elif cmd[0][0]=='?':
      info(p, use_tt, use_iso, MMX)
    elif cmd[0][0]=='u':
      undo(history, p.brd)
    elif cmd[0][0]=='g':
      p.genmove(genmoverequest(cmd), use_tt, use_iso, MMX)
    elif cmd[0][0]=='t':
      use_tt = not(use_tt)
      print('\nusing ' + msg(use_tt, use_iso))
    elif cmd[0][0]=='s':
      use_iso = not(use_iso)
      print('\nusing ' + msg(use_tt, use_iso))
    elif (cmd[0][0] in Cell.chars):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

def num_nodes(n):
  return sum([factorial(n)//factorial(k) for k in range(n+1)])

def tree_size():
  print('\nnumber of nodes in no-win ttt tree with k empty cells\n')
  for k in range(10):
    print('k', k, 'node', num_nodes(k))

tree_size()
interact(False, False)
