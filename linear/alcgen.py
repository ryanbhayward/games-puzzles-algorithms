# I think this is checking all forms that can
#   arise with alternating linear clobber

import sys
from paint_chars import paint3
from collections import deque
#from copy import deepcopy

BLACK, WHITE, EMPTY = 0,1,2
CHARS = 'xoq'  # black white g

def minstring(a,b):
  if len(a) < len(b): return a
  if len(b) < len(a): return b
  return min(a,b)

def opponent(ch):
  return '*' if ch == 'o' else 'o'

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

def revstring(s):
  return s[::-1]

def form(s, pattern, symbol):
  p = s.replace(pattern, symbol)
  while symbol*2 in p:
    p = p.replace(symbol*2, symbol)
  return p

def myadd(item, s):
  if item not in s and revstring(item) not in s: 
    s.add(item)

def nonzero(brd):
  return CHARS[BLACK] in brd and CHARS[WHITE] in brd

def clobber(brd):
  n = len(brd)
  newset = set()
  for j in range(2):
    stone = CHARS[j]
    for k in range(n-1):
      if (brd[k] == stone) and (brd[k] != brd[k+1]):
        b0, b1 = brd[:k], brd[k] + brd[k+2:]
        myadd(b0, newset)
        myadd(b1, newset)
    for k in range(1,n):
      if (brd[k] == stone) and (brd[k] != brd[k-1]):
        b0, b1 = brd[:k-1] + brd[k], brd[k+1:]
        myadd(b0, newset)
        myadd(b1, newset)
  return newset

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
   
def generate(startsize):
  qsize = 1
  fk = [[], []]
  for k in range(2):
    st = LC_state(startsize + k)
    show(st.b)
    q, spawn, forms = [st.b], [], []
    while len(q) > 0:
      brd = q.pop(0)
      newbrds = clobber(brd)
      for b in newbrds:
        if b not in spawn and \
            revstring(b) not in spawn \
            and nonzero(b): 
          print(paint3(b, CHARS))
          spawn.append(b)
          q.append(b)
          qsize += 1
          brev = revstring(b)
          fb    = form(b,     'xxo', 'q')
          fbrev = form(brev, 'xxo', 'q')
          fb = minstring(fb, fbrev)
          if fb not in forms:
            forms.append(fb)
    print('\nforms')
    for fb in sorted(forms):
      print(paint3(fb, CHARS))
      fk[k].append(fb)

  for k in range(2):
    print(fk[k])
    print()

  if equal(fk[0], fk[1]):
    print('equal lists, len', len(fk[0]))
  mydiff(fk[0], fk[1])
  print('\n  done, qsize', qsize)

generate(20) 
