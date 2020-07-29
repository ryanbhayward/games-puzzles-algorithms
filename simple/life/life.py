#!/usr/bin/env python3

"""
Conway's game of life    RBH 2020
"""

import numpy as np
import copy
from collections import deque
from paint import paint
from time import sleep

PTS = '.@#'
DEAD, ALIVE, GUARD = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[GUARD]

"""
string
"""
def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

"""
row-major order ... coord is 2-d, point is 1-d
"""

def coord_to_point(r, c, cols): return c + r*cols

def point_to_coord(p, cols): return divmod(p, cols)

"""
alpha-numeric labelling of coordinate points
"""

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def showboard(brd, R, C):  # with row and column labels
  pretty = '\n    ' 
  for c in range(C): # columns
    pretty += ' ' + paint(chr(ord('a')+c), PTS)
  pretty += '\n'
  for j in range(R): # rows
    if j < 10: pretty += ' '
    pretty += ' ' + paint(str(j), PTS) + ' '
    for k in range(C): # columns
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]], PTS)
    pretty += '\n'
  print(pretty)

def num_nbrs(s, j, cols, ch): # state, cell, columns, nbr-type
  num = 0
  if s[j-(cols+1)] == ch: num += 1
  if s[j- cols   ] == ch: num += 1
  if s[j-(cols-1)] == ch: num += 1
  if s[j-1       ] == ch: num += 1
  if s[j+1       ] == ch: num += 1
  if s[j+(cols-1)] == ch: num += 1
  if s[j+ cols   ] == ch: num += 1
  if s[j+ cols+1 ] == ch: num += 1
  return num

def next_state(s, cols):
  new = ''
  for j in range(len(s)):
    ch = s[j]
    if   ch == GCH: new += GCH
    else:
      m = num_nbrs(s, j, cols, ACH)
      if ch == ACH: new += ACH if m > 1 and m < 4 else DCH
      else:         new += ACH if m ==3           else DCH
  return new

"""
state of life
"""

class Livestate: 

# guard the board above, below, and at left 
# e.g. guarded 4x3 board   GGGG
#                          G.@.
#                          G..@
#                          G@@@
#                          G...
#                          GGGGG  <- don't forget last guard

  def __init__(self, rows, cols):
    newr, newc = rows+2, cols +1
    n = 1 + newr * newc       # cells + guards
    gb = PTS[DEAD]* n         # guarded board
    for j in range(newc):
      gb = change_str(gb, coord_to_point(0,      j, newc), GCH)
      gb = change_str(gb, coord_to_point(newr-1, j, newc), GCH)
    for j in range(1, newr):
      gb = change_str(gb, coord_to_point(j,      0, newc), GCH)
    gb = change_str(gb, n-1, GCH)  # last guard
    pairs = ((1,2), (2,3), (3,1), (3,2), (3,3)) # make these live
    for p in pairs:
      gb = change_str(gb, coord_to_point(p[0], p[1], newc), ACH)
    self.rows, self.cols, self.gb, self.n = newr, newc, gb, n

"""
input, output
"""

def interact():
  r, c = 15, 15
  itn, psn = 0, Livestate(r,c)
  while True:
    print('iteration', itn)
    showboard(psn.gb, psn.rows, psn.cols)
    #for j in range(1,r+1):
    #  for k in range(1,c+1):
    #    print(num_nbrs(psn.gb, coord_to_point(j,k,psn.cols), psn.cols, ACH), end=' ')
    #  print('')
    new = next_state(psn.gb, psn.cols)
    if new == psn.gb: break
    sleep(1.0)
    itn += 1
    psn.gb = new

interact()
