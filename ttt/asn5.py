# simple ttt solver  RBH 2022
#   - simplified version of ttt2
#       - only board rep'n is string (9 chars)
#       - no alpha-beta-negamax, only negamax
#       - easily modified to allow the first step towards alpha-beta:
#           return after win detection

from time import sleep

class Cell: # each cell is one of these: empty, x, o
  n, e, x, o = 9, '.', 'x', 'o'
  chars = e + x + o

def opponent(c):
  return Cell.x if c == Cell.o else Cell.o

# input-output ################################################
escape_ch   = '\033['
colorend    =  escape_ch + '0m'
textcolor   =  escape_ch + '0;37m'
stonecolors = (textcolor,\
               escape_ch + '0;35m',\
               escape_ch + '0;32m',\
               textcolor)

def printmenu():
  print('\n  h                help menu')
  print('  x b2            play x b 2')
  print('  o e3            play o e 3')
  print('  . a2             erase a 2')
  print('  ? x       solve, x-to-play')
  print('  u                     undo')
  print('  [return]              quit')

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
    pretty += ' ' + paint(str(1+j)) + '  ' 
    for k in range(3): 
      pretty += paint(psn.brd[j*3+k]) + ' '
    pretty += '\n'
  print(pretty)

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

def change_string(p, where, ch):
  return p[:where] + ch + p[where+1:]

Win_lines = ( # 8 winning lines, as location triples
    (0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

class Position: # ttt board with x,o,e cells

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
        print('\n  game over: ',Cell.chars[z],'wins\n')
        return True
    if Cell.e not in self.brd:
      print('\n  game over: draw\n')
      return True
    print('\n  game not yet over\n')
    return False

  def putstone(self, row, col, color):
    self.brd = change_string(self.brd, rc_to_lcn(row,col), color)

  def __init__(self):
    self.brd = Cell.e * Cell.n

  def makemove(self, cmd, H):
    parseok, cmd = False, cmd.split()
    if len(cmd)==2:
      ch = cmd[0][0]
      if ch in Cell.chars:
        q, n = cmd[1][0], cmd[1][1:]
        if q.isalpha() and n.isdigit():
          x, y = int(n) - 1, ord(q)-ord('a')
          if x>=0 and x < 3 and y>=0 and y < 3:
            self.putstone(x, y, ch)
            H.append(rc_to_lcn(x,y)) # add location to history
            return
          else: print('\n  coordinate off board')
    print('  ... ? ... sorry ...\n')

def undo(H, brd):  # pop last location, erase that cell
  if len(H)==0:
    print('\n    board empty, nothing to undo\n')
    return brd
  else:
    lcn = H.pop()
    brd = change_string(brd, lcn, Cell.e)
    return brd

####################### negamax search
def solverequest(cmd):
  cmd = cmd.split()
  invalid = (False, None, '\n invalid solve request\n')
  if len(cmd)==2:
    if cmd[1][0] == Cell.x or cmd[1][0] == Cell.o:
      return True, cmd[1][0], ''
  return invalid

def interact():
  p = Position()
  history = []  # used for erasing, so only need locations
  while True:
    showboard(p)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    if cmd[0][0]=='h':
      printmenu()
    elif cmd[0][0]=='u':
      p.brd = undo(history, p.brd)
    elif cmd[0][0]=='?':
      ok, ptm, msg = solverequest(cmd)
      if ok:
        result, calls = negamax(0, p, ptm)
        print(result, calls)
      else:
        print(msg)
    elif (cmd[0][0] in Cell.chars):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

interact()
