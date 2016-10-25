# hex player, based in part on Michi by Petr Baudis RBH 2016
import numpy as np

### cells ###############

class Cell: # each cell: empty, b, w  (bw for off-board corners)
  e,b,w,bw, ch = 0,1,2,3, '.*@-' 

def opponent(c): 
  return 3-c

### the board #####

# eg. 2x3 board     r,c                        positions

#  -***-     -1-1  -1 0  -1 1  -1 2  -1 3      0  1  2  3  4
#   o...o     0-1    0 0   0 1   0 2   0 3      5  6  7  8  9
#    o...o     1-1    1 0   1 1   1 2   1 3     10 11 12 13 14
#     -***-     2-1    2 0   2 1   2 2   2 3     15 16 17 18 19

class B:
  def __init__(self,r,c):
    self.r, self.c  = r, c  # rows, columns
    self.n  = r*c           # number of cells
    self.w  = self.c + 2    # add 1 row/col per border, W is width of padded board

    powers_of_3 = [1]
    for j in range(self.n-1): 
      powers_of_3.append(powers_of_3[j])
    self.powers_of_3 = np.array(powers_of_3)

    ### empty padded board
    self.empty = '\n'.join(['-' + self.c * '*' + '-'] + 
      self.r * ['@' + self.c * '.' + '@'] +
      ['-' + self.c * '*' + '-'])

    self.letters = 'abcdefghijklmnopqrstuvwxyz'

    # for colored output
    B.esc       = '\033['
    B.endcolor  =  B.esc + '0m'
    B.textcolor =  B.esc + '0;37m'
    B.color_of  = (B.textcolor, B.esc + '0;35m', B.esc + '0;32m', B.textcolor)

  def board_to_int(self,brd):
    return sum(brd*self.powers_of_3) # numpy multiplies vectors componentwise

  def rc_to_psn(self,r,c): 
    return (r + 1) * self.w + c + 1

  def psn_to_rc(self,psn):
    r,c = divmod(psn, self.w)
    return r-1, c-1

  def display(self,brd):
  #  -***-             a b c
  #  o...o            1 . . . o
  #  o...o    ==>      2 . . . o
  #  o...o              3 . . . o
  #  -***-               - * * * -

    d = '   ' + ' '.join(self.letters[0:self.c]) + '\n'
    X = ' '.join(brd).split('\n')
    for j in range(1,self.r+1): 
      d += ' '*j + '{:2d}'.format(j)+ X[j][2:] + '\n'
    d += ' '*(self.r+1) + X[self.r+1] + '\n'
    return d

  def paint(self,s):  # s   a string
    p = ''
    for c in s:
      x = Cell.ch.find(c)
      if x >= 0:
        p += self.color_of[x] + c + self.endcolor
      elif c.isalnum():
        p += self.textcolor + c + self.endcolor
      else: p += c
    return p

### user i-o

def tst(r,c):
  b = B(r,c)
  print(b.empty, '\n')
  print(b.paint(b.empty), '\n')
  print(b.display(b.empty))
  print(b.paint(b.display(b.empty)))

  for r in range(b.r):
    for c in range(b.c):
      p = b.rc_to_psn(r,c)
      print('{:2}'.format(p), end=' ')
      #print(r,c,psn_to_rc(p))
      assert (r,c) == (b.psn_to_rc(p))
    print('\n')
  print('\n')

  for p in range(b.w*(b.r+2)):
    print('{:3}'.format(p), end='')
    if b.psn_to_rc(p)[1]== b.c:
      print('\n')

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
  print('  x b2         play x b 2')
  print('  o e3         play o e 3')
  print('  . a2          erase a 2')
  print('  u                  undo')
  print('  ?           solve state')
  print('  g x/o           genmove')
  print('  t      use trans. table')
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
  if use_tt:
    b_int = board_to_int(psn.brd) 
    if b_int in AB[ptm-1]: 
      return AB[ptm-1][b_int], 0
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
    AB[ptm-1][b_int] = so_far
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
    if p.game_over():
      pass

tst(2,3)
