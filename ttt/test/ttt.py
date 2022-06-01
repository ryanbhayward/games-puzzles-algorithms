# stripped away features          RBH 2018
# negamax, no  alphabeta, no TT

import numpy as np

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

def printmenu():
  print('  h             help menu')
  print('  x b2         play x b 2')
  print('  o e3         play o e 3')
  print('  . a2          erase a 2')
  print('  ?           solve state')
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
#def ab_neg(AB, calls, d, psn, ptm, alpha, beta): # ptm: 1/0/-1 win/draw/loss
def negamax(calls, psn, ptm): # ptm: 1/0/-1 win/draw/loss
  calls += 1
  if psn.has_win(ptm):     
    return 1, calls  # previous move created win
  L = psn.legal_moves()
  if len(L) == 0:          
    return 0, calls  # board full, no winner
  so_far = -1  # best score so far
  for cell in L:
    psn.brd[cell] = ptm
    nmx, c = negamax(0, psn, opponent(ptm))
    so_far = max(so_far,-nmx)
    calls += c
    psn.brd[cell] = Cell.e   # reset brd to original
    # uncomment next 2 lines to early-abort when win detected
    if so_far == 1:  # found a win, cannot improve the result
      break
  return so_far, calls

def info(p):
    L = p.legal_moves()
    print('  legal moves', L)
    for cell in (Cell.x, Cell.o):
      print('  ',Cell.chars[cell], 'negamax',end='')
      nmx, c = negamax(0, p, cell)
      print('  result','{:2d}'.format(nmx), '  nodes',c)
    if p.game_over():
      pass

def interact():
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
      info(p)
    elif cmd[0][0]=='u':
      undo(history, p.brd)
    elif (cmd[0][0] in Cell.chars):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

interact()
