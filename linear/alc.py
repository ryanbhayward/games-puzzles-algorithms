# alternating linear clobber environment
# started 2025
# rbh

import sys
from paint_chars import paint3
from collections import deque
#from copy import deepcopy

BLACK, WHITE, EMPTY = 0,1,2  # black == LEFT  white == RIGHT
CHARS = 'xoq'  # black white g

def opponent(ch): return '*' if ch == 'o' else 'o'

def erase_stone(brd, psn, k):
  return brd[:psn] + CHARS[EMPTY]*k + brd[psn+k:]

def show(brd):
  indexstr = '   '  # print cell indices
  for j in range(len(brd)):
    if j < 10:
      indexstr += ' '
    indexstr += ' ' + str(j)

  cellstr = '   ' + ''.join(['  ' + c for c in brd])
  print(paint3('\n' + indexstr + '\n' + cellstr, CHARS))

def revstring(s): return s[::-1]

def myadd(item, s):
  if item not in s and revstring(item) not in s: 
    s.add(item)

def nonzero(brd):
  for j in range(len(brd)-1):
    if brd[j] != EMPTY and
       brd[j+1] != EMPTY and
       brd[j] == opponent(brd[j+1]): return True
  return False

class LC_state:
  def __init__(self, k):
    self.b =  'xxo'*k
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

def playGame(state):
  while True:
    show(state.b)
    m = get_command(CHARS[WHITE])
    if m == -3:
      break
    elif m == -1:
      print('sorry ? ... ')
    elif m == 0:
      clobber(state.b)
      break
  print('\n  adios ...\n  zaijian ...\n  sayonara ...\n  annyeong ...\n')

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
