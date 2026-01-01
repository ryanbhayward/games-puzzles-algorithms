#!/usr/bin/env python3
# - represent quarto state as sequence of 16 4-bit integers
# - simulate random games
# TODO: don't allow losing moves, as follows
#    - check any file with 3 tokens
#    - &sum tokens: if positive, then that value there wins
#    - &sum 15-complement of tokens: if positive, then that 15-comp't-value there wins
#    - remove winning pieces from list of possibles
#    - pick next piece randomly from each list of possibles (any piece if list empty)
# rbh v0 working 2025.12.31

from random import shuffle
from time import time

ROWS = 4
CELLS = ROWS*ROWS
FILES = ((0,1,2,3),(4,5,6,7),(8,9,10,11),(12,13,14,15),
         (0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),
         (0,5,10,15),(3,6,9,12))
NFILES = len(FILES)
TRIALS = 100000

def index_list():
  return list(range(CELLS))

def rperm():
  p = index_list()
  shuffle(p)
  return p

def show_row(r):
  for j in range(CELLS):
    print('{:2}'.format(r[j]), end=' ')
  print()
  
def show_perms(p, q):
  inds = index_list()
  show_row(inds)
  show_row(p)
  show_row(q)

def make_move(state, where, what):
  state[where] = what

def init_state():
  return CELLS*[-1]

def mybin(k):
  if k < 0:
    return(' -- ')
  return ('000' + bin(k)[ROWS-2:])[-ROWS:]

def show_st(st):
  print()
  for k in range(CELLS):
    print(mybin(st[k]), end=' ')
    if (k%ROWS) == ROWS-1:
      print()

def same_bit(x,y,psn):
  return (x >> psn) &1 == (y >> psn) &1

def wins(f, st, verb): # is file f a winning file?
  file = FILES[f]
  for j in range(ROWS):
    if st[file[j]] < 0: 
      return False
  for psn in range(ROWS-1):
    if same_bit(st[file[0]], st[file[1]], psn) and \
       same_bit(st[file[0]], st[file[2]], psn) and \
       same_bit(st[file[0]], st[file[3]], psn):
      if verb: show_st(st)
      if verb: print('\n', f, ' is winning file\n', sep='')
      return True
  return False

def has_win(st, verb):
  for f in range(NFILES):
    if wins(f, st, verb):
      return True
  return False

def play_game(verb):
  st = init_state()
  lcns = rperm()
  pieces = rperm()
  for j in range(3):
    make_move(st, lcns[j], pieces[j])
  for j in range(3, CELLS):
    make_move(st, lcns[j], pieces[j])
    if has_win(st, verb):
      if verb: show_perms(lcns, pieces)
      if verb: print('winmove ',j,': piece ',pieces[j],' at cell ',lcns[j],sep='')
      return j
  if verb: print('draw: no winning move')
  return 0 

def show_winmoves(wm):
  for j in range(CELLS):
    print('{:3}'.format(j), end=' ')
  print()
  for j in range(CELLS):
    print('{:3}'.format(wm[j]), end=' ')
  print()

t0 = time()
verb = False
winmoves = CELLS*[0]
for _ in range(TRIALS):
  x = play_game(verb)
  winmoves[x] += 1
print()
show_winmoves(winmoves)
p1, p2 = 0, 0
for j in range(1, CELLS):
  if j%2 == 1: p2 += winmoves[j]
  else: p1 += winmoves[j]
print('p1-wins  p2-wins  draws  total')
print(p1, '  ', p2, '  ', winmoves[0], TRIALS)
print('time in seconds', '{:.1f}'.format(time()-t0)) 
