# simple program to play linear clobber
import sys
from paint_chars import paint3
from collections import deque
#from copy import deepcopy

BLACK, WHITE, EMPTY = 0,1,2
CHARS = 'xog'  # black white g

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
  #print(paint3(indexstr + '\n' + cellstr + '\n' + brd, CHARS))
  print(paint3('\n' + indexstr + '\n' + cellstr, CHARS))

def reverse(s):
  return s[::-1]

def form(s, pattern, symbol):
  p = s.replace(pattern, symbol)
  while symbol*2 in p:
    p = p.replace(symbol*2, symbol)
  return p

def myadd(item, s):
  if item not in s and reverse(item) not in s: 
    s.add(item)

def clobber(brd):
  n = len(brd)
  newset = set()
  for j in range(2):
    stone = CHARS[j]

    #print('\n', paint3(stone, CHARS), ' clobbers forward\n', sep='')
    for k in range(n-1):
      if (brd[k] == stone) and (brd[k] != brd[k+1]):
        b0, b1 = brd[:k], brd[k] + brd[k+2:]
    #    print(k, paint3(b0, CHARS),  paint3(b1, CHARS))
    #    b0, b1 = form(b0, 'xxo', 'g'), form(b1, 'xxo', 'g')
    #    print(k, paint3(b0, CHARS),  paint3(b1, CHARS))
        myadd(b0, newset)
        myadd(b1, newset)

    #print('\n', paint3(stone, CHARS), ' clobbers backwards\n', sep='')
    for k in range(1,n):
      if (brd[k] == stone) and (brd[k] != brd[k-1]):
        b0, b1 = brd[:k-1] + brd[k], brd[k+1:]
    #    print(k, paint3(b0, CHARS),  paint3(b1, CHARS))
    #    b0, b1 = form(b0, 'xxo', 'g'), form(b1, 'xxo', 'g')
    #    print(k, paint3(b0, CHARS),  paint3(b1, CHARS))
        myadd(b0, newset)
        myadd(b1, newset)
  return newset

class LC_state:
  def __init__(self):

    # board as string
    self.b =  'xxo'*3
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

st = LC_state()
show(st.b)
q, spawn = [st.b], set()
while len(q) > 0:
  brd = q.pop(0)
  newbrds = clobber(brd)
  for b in newbrds:
    if b not in spawn and reverse(b) not in spawn:
      print(paint3(b, CHARS))
      spawn.add(b)
      q.append(b)
print('\ndone')

#clobber(st.b)
#playGame(brd)
