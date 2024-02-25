# play nim RBH 2016
# **   revised rbh 2024
# **   - use python bin()
# **   - def xorsum(L):  return reduce(ixor, L)

# solve value (and report all winning moves) using xor formula
# runtime proportional to total number of bits,
#   so can handle big piles

from sys import stdin
from string import ascii_letters as letters
from operator import ixor
from functools import reduce

class Nimgame:
# piles:  initial nim state,  eg ( 3, 5, 7 )
# state:  current nim state,  eg [ 3, 5, 7 ]

  def __init__(self):
    def get_piles():
      while True:
        raw = input('\nwelcome :) ...  pile sizes (eg. 3 5 7)   ')
        try:
          dim = tuple( int(x) for x in raw.split() )
          if len(dim) > 0 and all(d >= 0 for d in dim):
            return dim
        except ValueError: 
          pass
        print('invalid, try again')

    self.piles = get_piles()
    self.state = list(self.piles)
    self.n, self.maxpile = len(self.piles), max(self.piles)
    self.digits, self.bits = len(str(self.maxpile)), len(bin(self.maxpile))

  def gameover(self):
    return self == 0

  def showboard(self):
    print()
    for j in range(self.n): 
      pile = self.state[j]
      print(' ', letters[j], '  ',
        '{num:{width}}'.format(num=pile, width=self.digits), end= '')
      bj = bin(pile)[2:] # omit leading '0b'
      print(' ', '  '*(self.bits - len(bj)), ' '.join(bj))
    nimsum = xorsum(self.state)
    print(' sum  ',
        '{num:{width}}'.format(num=nimsum, width=self.digits), end='')
    bsum = bin(nimsum)[2:]
    print(' ', '  '*(self.bits - len(bsum)), ' '.join(bsum), '\n')

  def makemove(self, cmd):
    if len(cmd) < 2 or not cmd[1].isdigit() or len(cmd[0])!=1:
      print('\n  invalid request: move format a 1\n')
      return
    pile, n = ord(cmd[0])-ord('a'), int(cmd[1])
    if pile < 0 or pile > self.n:
      print('invalid pile')
      return
    if n < 1 or n > self.state[pile]:
      print('\n   cannot take that many from pile',cmd[0])
      return
    self.state[pile] -= n

def printmenu():
  print('\n  a 2      remove  2  stones from pile a')
  print('  ?        show all winmoves')
  print('  h        help -- print this menu')
  print('  [return]          quit\n')

def xorsum(L): return reduce(ixor, L)
  #xsum = 0
  #for j in L: xsum ^= j
  #return xsum

def nimreport(P): # report all winning nim moves from P, use formula
  print(' reduce a pile with k stones to k+sum stones ?')
  total = xorsum(P)
  if total==0:
    print('\n no: loss')
    return
  for j in P:
    tj = total^j
    if j >= tj: 
      print('\n yes: take',j - tj,'from pile with',j)

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
    elif cmd[0][0] in 'hH':
      printmenu()
      g.showboard()
    elif cmd[0][0]=='!' or cmd[0][0]=='?':
      nimreport(g.state)
    else: 
      cmd = cmd.split()
      g.makemove(cmd)

playgame()
