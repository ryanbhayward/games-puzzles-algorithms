#!/usr/bin/env python3

"""
Conway's game of life    RBH 2020
"""

import numpy as np
import copy
from collections import deque
from paint import paint
from time import sleep
from sys import stdin

PTS = '.*#'
DEAD, ALIVE, GUARD = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[GUARD]

def get_board(rows, cols): # if needed, add extra rows/cols
  B = []
  for line in stdin:
    B.append(line.rstrip().replace(' ',''))
  brows, bcols = len(B), len(B[0])
  for j in range(1, brows): assert(len(B[j]) == bcols)
  if bcols < cols: # append extra columns
    for j in range(brows): B[j] += DCH * (cols - bcols)
    bcols = cols
  if brows < rows: # append extra rows
    for j in range(rows-brows): B.append(DCH * bcols)
    brows = rows
  return B, brows, bcols

# add guards: top row, left column, bottom row (with one extra)
# original board        guarded board
#                          GGGG
#   .x.                    G.x.
#   ..x                    G..x
#   xxx                    Gxxx
#   ...                    G...
#                          GGGGG  <- don't forget last guard
def add_guards(B, r, c):
  B.insert(0, GCH * (1 + c))
  for j in range(r): B[j+1] = GCH + B[j+1]
  B.append(GCH * (2 + c))
  return(''.join(B), len(B), len(B[0]))

"""
replace char-in-string
"""

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

"""
row-major order ... coord is 2-d, point is 1-d
"""

def coord_to_point(r, c, cols): return c + r*cols

def point_to_coord(p, cols): return divmod(p, cols)

#alpha-numeric labelling of coordinate points
def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

# add numeric row indices, alphabetic column indices
def showboard(brd, R, C): 
  pretty = '\n    ' 
  for c in range(C): # columns
    pretty += ' ' + paint(chr(ord('a')+c), PTS)
  pretty += '\n'
  for j in range(R): # rows
    if j < 10: pretty += ' '
    pretty += ' ' + paint(str(j), PTS) + ' '
    for k in range(C): # columns
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]], PTS)
    if j == R-1: # in last row, put last guard
      pretty += ' ' + paint(brd[R*C], PTS)
    pretty += '\n'
  print(pretty)

""" 
Conway's next-state formula
"""

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

class Livestate: 

  def __init__(self, rows, cols):
    b, r, c = get_board(rows, cols)
    self.gb, self.rows, self.cols = add_guards(b, r, c)
    self.n = self.rows*self.cols + 1
    print(len(self.gb), self.n)
    assert(len(self.gb) == self.n)

"""
input, output
"""

def interact():
  r, c = 20, 25
  itn, psn = 0, Livestate(r,c)
  while True:
    print('iteration', itn)
    showboard(psn.gb, psn.rows, psn.cols)
    new = next_state(psn.gb, psn.cols)
    if new == psn.gb: break
    sleep(.1)
    itn += 1
    psn.gb = new

interact()
