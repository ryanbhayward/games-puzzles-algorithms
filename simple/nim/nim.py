# play nim RBH 2016
# under construction
from sys import stdin
from time import sleep
from random import randint

def sorted(L):
  return all(L[j] <= L[j+1] for j in range(len(L)-1))

def numdiff(L,M): # number of different entries
  assert(len(L)==len(M))
  count = 0
  for j in range(len(L)):
    if L[j] != M[j]: count += 1
  return count

class Nimgame:
# dim: original pile sizes, as coordinates  eg. [ 3, 5, 7 ]
# M: multiplier cooefficients to convert from coord to psn,
#    eg. [ (7+1)*(5+1), (7+1), (0+1) ]
# state: current pile sizes, as psn
# for states, convert between 
#    coordinates          eg. [ 1, 0, 4]  and
#    psns (linear offset) eg. 1 * M[0] + 0 * M[1] + 4 * M[2]
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
    print('\n')
    st = self.crd(self.state)
    for j in range(self.rows):
      for k in range(self.cols):
        if j + st[k] >= self.rows: print('*',end='   ')
        else:                 print(' ',end='   ')
      print('')
    print('')
    for k in range(len(st)):
      print(chr(ord('a')+k), end='   ')
    print('')
    for k in st:
      print(k, end='   ')
    print('')
    print('')

  def makemove(self, cmd):
    if len(cmd) < 2 or not cmd[1].isdigit() or len(cmd[0])!=1:
      print('  invalid request: move format a 1\n')
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
    if not sorted(coords):
      self.showboard()
      coords.sort()
      self.state = self.psn(coords)
      print('sort columns, relabel')


  def __init__(self):
    def solve(j, cj):
      print('solving',cj,end=': ')
      for k in range(j):
        ck = self.crd(k)
        ck.sort()
        if numdiff(cj,ck)==1 and not self.wins[k]:
          print('to',ck,'wins')
          self.wins[j], self.winmove[j] = True, k
          sleep(.1)
          return
      print('')

    while True:
      dim = input('nim game pile sizes (eg. 3 5 7)   ')
      try:
        self.dim = tuple( int(x) for x in dim.split() )
        if len(self.dim) > 0 and all(d >= 0 for d in self.dim):
          break
        else:
          print('invalid, try again')
      except ValueError: 
        print('invalid, try again')
    self.rows, self.cols = max(self.dim), len(self.dim)
    m, self.M = 1, [1]
    for j in reversed(self.dim):
      m = m*(j+1)
      self.M.append(m)
    self.M.pop()
    self.M.reverse()
    print(self.M)
    self.state = self.psn(self.dim)
    self.showboard()
    rc = [ randint(0,d) for d in self.dim ]
    print(rc, self.psn(rc), self.psn((0,0,0)), self.psn(self.dim))
    
    self.size = 1
    for j in self.dim:  self.size *= j+1
    self.wins, self.winmove = [False]*self.size, [None]*self.size
    #print(self.size)
    #print(self.wins)
    #for j in range(self.size):
    #  print(j, self.crd(j))
    for j in range(1, self.size+1):
      cj = self.crd(j)
      if sorted(cj): solve(j,cj)
        #print(cj,self.wins[j])

def playgame():
  g = Nimgame()
  while True:
    g.showboard()
    if g.gameover():
      print('\ngame over!  player who just moved wins ...\n')
      return
    cmd = input('')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='h':
      print('a 2      remove 2 stones from pile a')
      print('?        generate computer move')
      print('h        help')
      print('[return] quit')
      g.showboard()
    elif cmd[0][0]=='?':
      print('computer move:', end=' ')
      if g.wins[g.state]:
        print('win to', g.crd(g.winmove[g.state]))
      else:
        print('lose')
    else: 
      cmd = cmd.split()
      g.makemove(cmd)

playgame()
