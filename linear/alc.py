# alternating linear clobber environment
# started 2025
# rbh

# TODO: allow specified user move

import sys
#import string
from paint_chars import paint3
from collections import deque
#from copy import deepcopy

BLK, WHT, EMP = 0,1,2  # b LEFT, w RIGHT
CHRS = 'xo_'  # black white g

def direction(right):
  return 'right' if right else 'left '

def opp_ch(ch): return 'x' if ch == 'o' else 'o'

def opponent(col): return 1 - col

def color(brd, psn, color):
  return brd[:psn] + CHRS[color] + brd[psn+1:]

def clobber(brd, psn, n, rgt): # if rgt, clobber right
  print(psn, 'clobber', direction(rgt), end='  ')
  delta = 1 if rgt else -1
  if (psn + delta < 0) or (psn + delta >= n):
    print('off board')
    return ''
  bp, bpd = brd[psn], brd[psn + delta]
  if (bp == EMP or bpd == EMP or bp == bpd):
    print('invalid there')
    return ''
  b1 = color(brd, psn, EMP)
  col = CHRS.index(b1[psn + delta])
  return color(b1, psn + delta, opponent(col))

def show(brd):
  indexstr = '   '  # print cell indices
  for j in range(len(brd)):
    if j < 10:
      indexstr += ' '
    indexstr += ' ' + str(j)

  cellstr = '   ' + ''.join(['  ' + c for c in brd])
  print(paint3('\n' + indexstr + '\n' + cellstr, CHRS))

def revstring(s): return s[::-1]

def myadd(item, s):
  if item not in s and revstring(item) not in s: 
    s.add(item)

def nonzero(brd):
  for j in range(len(brd)-1):
    if brd[j] != EMP and \
       brd[j+1] != EMP and \
       brd[j] == opp_ch(brd[j+1]): return True
  return False

class ALC:
  def __init__(self, k):
    self.b =  'ox'*k
    self.n = len(self.b)

def get_command(color):
  print('\n ' + color + '  command? ', end='')
  line = sys.stdin.readline()
  print('')
  if line[0] == '\n':
    return -3  # end game
  elif not line.split()[0].isdigit():
    return -1  # bad input, retry
  elif line.split()[0] == 'c':
    return 0  # clobber
  else:
    return int(line.split()[0])

def test(brd):
  n = len(brd)
  for j in range(n):
    for k in (0,1):
      cr = clobber(brd, j, n, (True,False)[k])
      if cr: print(paint3(cr, CHRS))

def playGame(state):
  while True:
    show(state.b)
    m = get_command(CHRS[WHT])
    if m == -3:
      break
    elif m == -1:
      print('sorry ? ... ')
    elif m == 0:
      test(state.b)
    break
  #print('\n  adios ...\n  zaijian ...\n  sayonara ...\n  annyeong ...\n')
  print('\n  adios ...')

def equal(a,b):
  lena, lenb = len(a), len(b)
  if lena != lenb:
    print('unequal length lists', lena, lenb)
    return False
  for j in range(lena):
    if a[j] != b[j]:
      print('unequal at index',j, a[j], b[j])
      return False
  return True

def mydiff(sa, sb):
  for x in sa:
    if x not in sb: print('in L0 not L1', x)
  for x in sb:
    if x not in sa: print('in L1 not L0', x)

state = ALC(5)
show(state.b)
playGame(state)
