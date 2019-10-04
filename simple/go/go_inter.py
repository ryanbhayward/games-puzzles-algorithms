# interactive 3x3 go player    RBH 2018
# scores position
# does not make legal moves yet

import numpy as np

class Cell: # each cell is one of these: empty, b, w
  n,e,b,w,chars = 9,0,1,2,'.*o' 

def opponent(c): return 3-c
# each cell is 0,1,2
# so number positions == 3**9
# can represent position as 9-digit base_3 number

num_psns = 19683  # 3**Cell.n
powers_of_3 = np.array( # for converting position to base_3 int
  [1, 3, 9, 27, 81, 243, 729, 2187, 6561], dtype=np.int16)

def board_to_int(B):
  return sum(B*powers_of_3) # numpy multiplies vectors componentwise

# convert from integer for board position
def base_3( y ): 
  assert(y <= num_psns)
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
  print(' h       help menu')
  print(' * b2    play black b 2')
  print(' o e3    play white e 3')
  print(' . a2    erase      a 2')
  print(' s       score')
  print(' u       undo')
  print('[return] quit')

def printscore(p):
  print(' current score (black - white) = ', p.score())

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
  for j in range(2,-1,-1): # rows
    pretty += ' ' + paint(str(1+j)) + ' '
    for k in range(3): # columns
      pretty += ' ' + paint(Cell.chars[psn.brd[rc_to_lcn(j,k)]])
    pretty += '\n'
  print(pretty)

##################### position ########################
# cell indices, or locations:
#   6 7 8
#   3 4 5
#   0 1 2

Neighbours = [[1,3],[0,2,4],[1,5],[0,4,6],[1,3,5,7],[2,4,8],[3,7],[4,6,8],[5,7]]

def rc_to_lcn(r,c): 
  return r*3 + c

def lcn_to_alphanum(p):
  r, c = divmod(p,3)
  return 'abc'[c] + '123'[r]

#def makemove(p, cell, position, h): # assume cell empty
  #putstone(p, cell, position) # cell in position gets color p
  #removecaptured(opponent(p), cell, position) 
  #if 0 == liberties(cell, position): return(ILLEGAL) # suicide 
  #if in_history(position, h):        return(ILLEGAL) # superko 
  #h.append(position) # add new position to move history

class Position: # 3x3 go board with x,o,e cells
  def score(self): # return Tromp-Taylor position score
    b,w = 0,0 # points for black, white
    seen = [False]*Cell.n  # all cells start unseen
    for c in range(Cell.n):   # for each cell on the board
      if   self.brd[c] == Cell.b: b+=1  # c is a black stone
      elif self.brd[c] == Cell.w: w+=1  # c is a white stone
      elif not seen[c]: # an empty cell we have not yet seen
        reach_b, reach_w, cells = False, False, 0
        seen[c] = True ; L = [c]
        while len(L)>0:
          t = L.pop()
          cells += 1
          for u in Neighbours[t]:
            if   self.brd[u] == Cell.b: reach_b = True
            elif self.brd[u] == Cell.w: reach_w = True
            elif not seen[u]: seen[u] = True ; L.append(u)
        if   reach_b and not reach_w: b+= cells
        elif reach_w and not reach_b: w+= cells
    return b-w

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

def interact(use_tt):
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
    elif cmd[0][0]=='s':
      printscore(p)
    elif cmd[0][0]=='u':
      undo(history, p.brd)
    elif (cmd[0][0] in Cell.chars):
      p.makemove(cmd, history)
    else:
      print('\n ???????\n')
      printmenu()

interact(False)
