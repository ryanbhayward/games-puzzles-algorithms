# play nim RBH 2016
# under construction
from sys import stdin
from time import sleep
from random import randint

class Nimgame:
  def psn(self, coord):
    return sum([a*b for a,b in zip(coord,self.M)])

  def __init__(self):
    while True:
      dim = input('nim game pile sizes (eg. 3 5 7)   ')
      try:
        self.dim = [ int(x) for x in dim.split() ]
        if len(self.dim) > 0 and all(d >= 0 for d in self.dim):
          break
        else:
          print('invalid, try again')
      except ValueError: 
        print('invalid, try again')
    print(self.dim)
    m, self.M = 1, [1]
    for j in reversed(self.dim):
      m = m*(j+1)
      self.M.append(m)
    self.M.pop()
    self.M.reverse()
    print(self.M)
    rc = [ randint(0,d) for d in self.dim ]
    print(rc, self.psn(rc), self.psn((0,0,0)), self.psn(self.dim))

def psn(coord, multiplier):
  return sum([a*b for a,b in zip(coord,multiplier)])

def showboard(L):
  if gameover(L): 
    return
  print('\n  ',end='')
  for j in range(len(L)):
    if L[j] > 0: print('*'*L[j], end='  ')
  print('\n  ',end='')
  for j in range(len(L)):
    if L[j] > 0: print(chr(j+ord('a')), L[j], end='   ')
  print('\n')

def gameover(L):
  for j in L:
    if j>0: return False
  return True

def makemove(c,n,L):
  pile = ord(c)-ord('a')
  if pile<0 or pile >= len(L):
    print('invalid pile')
  elif n<1 or n>L[pile]:
    print('\n   cannot take that many from pile',c)
  else:
    #print('\n ',n,'from pile',c)
    L[pile] -= n
  showboard(L)

def playgame():
  L = [3,5,7]
  showboard(L)
  while True:
    if gameover(L):
      print('\ngame over!  player who just moved wins ...\n')
      return
    cmd = input('')
    if len(cmd)==0 or cmd[0]=='q':
      print('\n ... adios :)\n')
      return
    elif cmd[0][0]=='h':
      print('a 2     remove 2 stones from pile a')
      print('?       generate computer move')
      print('h       help')
      print('q       quit')
      showboard(L)
    else: 
      cmd = cmd.split()
      if len(cmd)<2 or not cmd[1].isdigit():
        print('  move format: a 1\n')
      else:
        makemove(cmd[0][0], int(cmd[1]), L)

#playgame()
g = Nimgame()
