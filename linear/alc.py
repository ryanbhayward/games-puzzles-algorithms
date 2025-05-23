# alternating linear clobber environment
# started 2025
# rbh

# TODO: add pattern names

import sys
from paint_chars import paint3
from collections import deque
from copy import copy

BLK, WHT, EMP = 0,1,2  # b LEFT, w RIGHT
CHRS = 'xo_'  # black white g

class ALC:
  def __init__(self, k):
    self.b =  'ox'*k

def opp_ch(ch): 
  cell = CHRS.index(ch)
  assert(ch != EMP)
  return CHRS[BLK] if cell == WHT else CHRS[WHT]

def change_str(brd, psn, ch):
  return brd[:psn] + ch + brd[psn+1:]

def revstring(s): return s[::-1]

def direction(right):
  return 'right' if right else 'left '

def clobber(brd, psn, delta):
  b = change_str(brd, psn + delta, brd[psn])
  b = change_str(b,   psn,        CHRS[EMP])
  return b

def show(brd):
  indexstr = '   '  # print cell indices
  for j in range(len(brd)):
    if j < 10:
      indexstr += ' '
    indexstr += ' ' + str(j)
  cellstr = '   ' + ''.join(['  ' + c for c in brd])
  print(paint3('\n' + indexstr + '\n' + cellstr, CHRS))

def error(oops):
  if oops == 'mv_format':
    print(' enter move like this    13+')
    print('              or this     0-')
  elif oops == 'off_board':
    print(' invalid: off board')
  elif oops == 'empty':
    print(' that location empty')
  elif oops == 'nbr':
    print(' stone must touch nbr')
  elif oops == 'nbr_emp':
    print(' neighbor empty')
  else:
    print(' ??? unknown error')
  return ''

def undo(H, brd):  # pop last meta-move
  if len(H)==1:
    print('\n    original position,  nothing to undo\n')
    return brd
  else:
    H.pop()
    return copy(H[len(H)-1])

def requestmove(brd, cmd):
  parseok = False
  n = len(brd)
  psn, direction = cmd[:-1], cmd[-1]
  if (cmd[-1] not in '+-') or not psn.isdigit():
    return error('mv_format')
  psn = int(psn)
  if psn < 0 or psn >= n:
    return error('off_board')
  if brd[psn] == CHRS[EMP]:
    return error('empty')
  if psn == 0 and direction == '-' or \
     psn >= n - 1 and direction == '+':
    return error('off_board')
  delta = 1 if direction=='+' else -1
  if brd[psn] == CHRS[EMP]:
    return error('nbr_emp')
  if brd[psn] != opp_ch(brd[psn + delta]):
    return error('nbr')
  return clobber(brd, psn, delta)

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

def interact(brd):
  history = []  # board positions
  new = copy(brd); history.append(new)
  while True:
    show(brd)
    cmd = input(' ')
    if len(cmd)==0:
      print('\n ... adios :)\n')
      return
    #if cmd[0][0]=='h':
    #  printmenu()
    elif cmd[0][0]=='u':
      brd = undo(history, brd)
    else:
      new = requestmove(brd, cmd)
      if new != '':
        brd = new
        history.append(new)

state = ALC(3)
interact(state.b)
