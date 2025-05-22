# alternating linear clobber environment
# started 2025
# rbh

# TODO: clobber not working properly

import sys
#import string
from paint_chars import paint3
from collections import deque
from copy import copy

BLK, WHT, EMP = 0,1,2  # b LEFT, w RIGHT
CHRS = 'xo_'  # black white g

def direction(right):
  return 'right' if right else 'left '

def opp_ch(ch): return 'x' if ch == 'o' else 'o'

def opponent(col): return 1 - col

def color(brd, psn, color):
  return brd[:psn] + CHRS[color] + brd[psn+1:]

def undo(H, brd):  # pop last meta-move
  if len(H)==1:
    print('\n    original position,  nothing to undo\n')
    return brd
  else:
    H.pop()
    return copy(H[len(H)-1])

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

def show_format():
  print('invalid move format')
  print('  like this: 13+')
  print('... or this: 0-')

def clbbr(brd, psn, delta):
  b1 = color(brd, psn, EMP)
  col = CHRS.index(b1[psn + delta])
  return color(b1, psn + delta, opponent(col))

def requestmove(brd, cmd):
  parseok = False
  psn, direction = cmd[:-1], cmd[-1]
  if (cmd[-1] not in '+-') or not psn.isdigit():
    show_format()
    return ''
  psn = int(psn)
  if psn == 0 and direction == '-' or \
     psn >= len(brd) - 1 and direction == '+':
    print('invalid move: off board')
    return ''
  delta = 1 if direction else -1
  return clbbr(brd, psn, delta)

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

def interact(brd):
  history = []  # board positions
  new = copy(brd); history.append(new)
  while True:
    show(brd)
    cmd = input(' ')
    print(cmd)
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    #if cmd[0][0]=='h':
    #  printmenu()
    elif cmd[0][0]=='u':
      brd = undo(history, brd)
    elif (cmd[0][0].isdigit()):
      new = requestmove(brd, cmd)
      if new != '':
        brd = new
        history.append(new)

state = ALC(3)
interact(state.b)
