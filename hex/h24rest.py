
def show_parent(P):
  print(disp_parent(P))

######## positions <------>   row, column coordinates

def psn_of(x,y):
  return x*B.c + y

def rc_of(p): # return usual row, col coordinates
  return divmod(p, B.c)

### mcts ########################################

def legal_moves(board):
  L = []
  for psn in range(B.fat_n):
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
  board, history = deepcopy(Board.empty_fat_brd), []
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

#big_tst()
interact()
