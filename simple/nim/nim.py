# play nim RBH 2016
# solve values using dynamic programming
# ... exercise: solve values using exclusive or :)

from sys import stdin
from copy import deepcopy
from operator import xor

class Nimgame:
#        two different state representations
# - coordinates: eg. [ 1, 0, 4 ]     vector of current pile sizes
# - psn:         eg.  52    linear "offset" of coordinates
#                  52 = 1 * M[0] + 0 * M[1] + 4 * M[2]
# dim:  original pile sizes, as coordinates  eg. [ 3, 5, 7 ]
# M:    multiplier coefficients, used in coord-to-psn conversion
#            eg. M = [ (7+1)*(5+1), (7+1), (0+1) ]
# state:  current pile sizes, as psn

  def gameover(self):
    return self.state == 0

  def psn(self, coord):
    return sum([a*b for a,b in zip(coord,self.M)])

  def crd(self, psn):
    r, crd = psn, []
    for j in self.M:
      d = r // j
      r = r - d*j
      crd.append(d)
    return crd

  def showboard(self):
    st = self.crd(self.state)
    print('\n')
    for j in range(max(st)):
      rowstr = ' '
      for k in range(self.cols):
        if j + st[k] >= max(st): rowstr += '*   '
        else:                    rowstr += '    '
      print(rowstr)
    rowstr = ' '
    for k in range(len(st)):
      rowstr += chr(ord('a')+k) + '   '
    print(rowstr)
    rowstr= ' '
    for k in st:
      if k>0: rowstr += str(k) + '   '
      else:   rowstr +=         '    '
    print(rowstr,'\n')

  def makemove(self, cmd):
    if len(cmd) < 2 or not cmd[1].isdigit() or len(cmd[0])!=1:
      print('\n  invalid request: move format a 1\n')
      return
    pile, n = ord(cmd[0])-ord('a'), int(cmd[1])
    if pile < 0 or pile > self.cols:
      print('invalid pile')
      return
    coords = self.crd(self.state)
    if n < 1 or n > coords[pile]:
      print('\n   cannot take that many from pile',cmd[0])
      return
    coords[pile] -= n
    self.state = self.psn(coords)

  def __init__(self):
    def solveall():
      print('\ngame initialization: find all position win/loss values')
      # for each losing state, find winning states that reach it
      for j in range(len(self.wins) - 1): # nothing reaches last state
        if not self.wins[j]: # loss, so find all psns that reach j
          cj = self.crd(j)
          #print(cj,'loses, find all wins that reach this')
          for x in range(len(cj)):
            cjcopy = deepcopy(cj)
            for t in range(1+cj[x], 1+self.dim[x]):
              cjcopy[x] = t
              pjc = self.psn(cjcopy)
              self.wins[pjc], self.winmove[pjc] = True, j
      print('')

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

    def initmultiplier(dim):
      m, M = 1, [1]
      for j in reversed(dim):
        m = m*(j+1)
        M.append(m)
      M.pop()
      M.reverse()
      return M

    self.dim = getdim()
    self.rows, self.cols = max(self.dim), len(self.dim)
    self.M = initmultiplier(self.dim)
    self.state = self.psn(self.dim)
    self.showboard()
    
    self.size = 1
    for j in self.dim:  self.size *= j+1
    self.wins, self.winmove = [False]*self.size, [None]*self.size
    solveall()

def printmenu():
  print('nim game commands')
  print('  a 2      remove  2  stones from pile a')
  print('  ?        value, one winmove, dp algorithm')
  print('  !        value, all winmoves, nim formula')
  print('  h        help -- print this menu')
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

def nimdpreport(g):
  if g.wins[g.state]:
    print(' win,  eg. to', g.crd(g.winmove[g.state]))
  else:
    print(' loss')

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
    elif cmd[0][0]=='h':
      printmenu()
      g.showboard()
    elif cmd[0][0]=='?':
      nimdpreport(g)
    elif cmd[0][0]=='!':
      nimreport(g.crd(g.state))
    else: 
      cmd = cmd.split()
      g.makemove(cmd)

playgame()
