# simple program to play linear clobber
import sys
from paint_chars import paint
from copy import deepcopy

BLACK, WHITE, EMPTY = 0,1,2
CHARS = 'xo-'  # black white empty

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
  #print(paint(indexstr + '\n' + cellstr + '\n' + brd, CHARS))
  print(paint('\n' + indexstr + '\n' + cellstr, CHARS))

def clobber(brd):
  n = len(brd)
  for j in range(2):
    stone = CHARS[j]
    print('\n', paint(stone, CHARS), ' clobbers forward\n', sep='')
    for k in range(n-1):
      if (brd[k] == stone) and (brd[k] != brd[k+1]):
        print(k, paint(brd[:k], CHARS),  paint(brd[k] + brd[k+2:], CHARS))
    print('\n', paint(stone, CHARS), ' clobbers backwards\n', sep='')
    for k in range(1,n):
      if (brd[k] == stone) and (brd[k] != brd[k-1]):
        print(k, paint(brd[:k-1] + brd[k], CHARS),  paint(brd[k+1:], CHARS))

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

brd = LC_state()
playGame(brd)
