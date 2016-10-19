# classic ttt: 3x3 board     RBH 2016
import numpy as np

class Cell: # each cell is one of these: empty, x, o
  e,x,o,n,chars = 0,1,2,9,'.xo' 

# each board position 0,1,2, so we can think of a board
#   position as a 9-digit number base 3
# so number of different states is same as max 9-digit base_3 integer
ttt_max_states = 19682  # 3**Cell.n - 1

# convert from integer for board position
def base_3( y ): 
  assert(y <= ttt_max_states)
  L = [0]*Cell.n
  for j in range(9):
    y, L[j] = divmod(y,3)
    if y==0: break
  return np.array( L, dtype = np.int8)

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
  print('  x b2         play X b 2')
  print('  o e3         play O e 3')
  print('  . a2         erase a 2')
  print('  g x/o           genmove')
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
      pretty += ' ' + paint(Cell.chars[psn.brd[rc_to_psn(j,k)]])
    pretty += '\n'
  print(pretty)
  print('hash ',psn.hash(),'  empty cells', psn.num_empty())

### position tuples of 8 symmetric ttt board permutations
Syms = ( (0,1,2,3,4,5,6,7,8),
         (0,3,6,1,4,7,2,5,8),
         (2,1,0,5,4,3,8,7,6),
         (2,5,8,1,4,7,0,3,6),
         (8,7,6,5,4,3,2,1,0),
         (8,5,2,7,1,4,6,3,0),
         (6,7,8,3,4,5,0,1,2),
         (6,3,0,7,4,1,8,5,2))

Win_lines = ( # psn tuples of 8 winning lines
  (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

# board positions
#   0 1 2
#   3 4 5
#   6 7 8
def rc_to_psn(r,c): return r*3 + c

class Position: # ttt board with x,o,e cells
  def legal_moves(self):
    L = []
    for j in range(Cell.n):
      if self.brd[j]==Cell.e: 
        L.append(j)
    return L

  def num_empty(self):
    return (self.brd == Cell.e).sum()
  
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
    self.brd[rc_to_psn(row,col)] = color

  # usual hash function
  # position 2 1 2 0 0 ... hashes to 2*3^0 + 1*3^1 + 2*3^2 ...
  # return min hash in set of 8 symmetric positions
  def hash(self):
    best = ttt_max_states + 1 # equivalent to plus infinity
    for j in range(len(Syms)):
      ttl, multiplier = 0, 1
      for t in Syms[j]:
        ttl += multiplier * self.brd[t]
        multiplier *=3
      best = min(best,ttl)
    return best

  def __init__(self, y):
    self.brd = np.array( base_3(y) )
    #print(self.brd)

  def genmove(self, request):
    if request[0]:
      print(' genmove coming soon')
    else:
      print(request[2])

  def makemove(self, cmd):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch in Cell.chars:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < 3 and y>=0 and y < 3:
            self.putstone(x, y, char_to_cell(ch))
            return
          else: print('\n  coordinate off board')
    print('  ... ? ... sorry ...\n')

def playgame():
  p = Position()
  while True:
    showboard(p)
    print('legal moves', p.legal_moves())
    if p.game_over():
      return
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='g':
      p.genmove(genmoverequest(cmd))
    elif (cmd[0][0] in Cell.chars):
        p.makemove(cmd)
    else:
      print('\n try again \n')

#playgame()
for j in range(20):
  p = Position(j)
  showboard(p)

for j in range(3**9):
  p = Position(j)

for j in reversed(range(10)): print(j)
