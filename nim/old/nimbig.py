# play nim RBH 2016
# solve value (and report all winning moves) using xor formula
# runtime proportional to total number of bits,
#   so can handle big piles

from sys import stdin
#from operator import xor

class Nimgame:
# dim:    starting nim state, eg (3, 5, 7)
# state:  current nim state, as list,  eg [ 1, 0, 4]

  def gameover(self):
    return all(j==0 for j in self.state)

  def showboard(self):
    print('\n ',end='')
    for j in self.state: print(j,end=' ')
    print('')
    rowstr = ' '
    for k in range(len(self.state)):
      rowstr += chr(ord('a')+k) 
      for j in range(len(str(self.state[k]))): 
        rowstr += ' '
    print(rowstr,'\n')

  def makemove(self, cmd):
    if len(cmd) < 2 or not cmd[1].isdigit() or len(cmd[0])!=1:
      print('\n  invalid request: move format a 1\n')
      return
    pile, n = ord(cmd[0])-ord('a'), int(cmd[1])
    if pile < 0 or pile > self.cols:
      print('invalid pile')
      return
    if n < 1 or n > self.state[pile]:
      print('\n   cannot take that many from pile',cmd[0])
      return
    self.state[pile] -= n

  def __init__(self):
    def getdim():
      while True:
        raw = input('nim game pile sizes (eg. 3 5 7)   ')
        try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim):
            return dim
        except ValueError: 
          pass
        print('invalid, try again')

    self.dim = getdim()
    self.rows, self.cols = max(self.dim), len(self.dim)
    self.state = []
    for j in self.dim: self.state.append(j)
    self.showboard()

def printmenu():
  print('nim game commands')
  print('  a 2      remove  2  stones from pile a')
  print('  ?        value, all winmoves, nim formula')
  print('  H        help -- print this menu')
  print('  [return]          quit')

def xorsum(L):
  xsum = 0
  for j in L: xsum ^= j
  return xsum

def nimreport(P): # report all winning nim moves from P, use formula
  total = xorsum(P)
  if total==0:
    print(' loss')
    return
  for j in P:
    tj = total^j
    if j >= tj: 
      print(' win: take',j - tj,'from pile with',j)

def playgame():
  g = Nimgame()
  printmenu()
  while True:
    g.showboard()
    if g.gameover():
      print('\n game over!  player who just moved wins ...\n')
      return
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='H':
      printmenu()
      g.showboard()
    elif cmd[0][0]=='!' or cmd[0][0]=='?':
      nimreport(g.state)
    else: 
      cmd = cmd.split()
      g.makemove(cmd)

playgame()
