#!/usr/bin/env python3

"""
Conway's game of life RBH 2020
TODO  init board, set rules
"""

import numpy as np
import copy
from collections import deque

"""
points on the board
"""

PTS = '.*#'
DEAD, ALIVE, GUARD = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[GUARD]

"""
board: a one-dimensional string

3x4 board indices 0  1  2  3        <- row 0
                  4  5  6  7        <- row 1
                  8  9 10 11        <- row 2
   
      columns     0  1  2  3
"""

def coord_to_point(r, c, C):
  return c + r*C

def point_to_coord(p, C):
  return divmod(p, C)

def point_to_alphanum(p, C):
  r, c = point_to_coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def change_str(s, where, what):
  return s[:where] + what + s[where+1:]

ROWS, COLS  =  12, 16
N = ROWS * COLS

NBRS = []
for r in range(ROWS):
  for c in range(COLS):
    nbs = []
    if r > 0:                nbs.append(coord_to_point(r-1, c,   COLS))
    if r > 0 and c < COLS-1: nbs.append(coord_to_point(r-1, c+1, COLS))
    if c > 0:                nbs.append(coord_to_point(r,   c-1, COLS))
    if c < COLS-1:           nbs.append(coord_to_point(r,   c+1, COLS))
    if r < ROWS-1 and c > 0: nbs.append(coord_to_point(r+1, c-1, COLS))
    if r < ROWS-1:           nbs.append(coord_to_point(r+1, c, COLS))
    NBRS.append(nbs)
print('nbrs', NBRS)

LFT_COL, RGT_COL, TOP_ROW, BTM_ROW = set(), set(), set(), set()

for r in range(ROWS):
  LFT_COL.add(coord_to_point(r, 0, COLS))
  RGT_COL.add(coord_to_point(r, COLS-1, COLS))

for c in range(COLS):
  TOP_ROW.add(coord_to_point(0, c, COLS))
  BTM_ROW.add(coord_to_point(ROWS-1, c, COLS))
#print(LFT_COL, RGT_COL, TOP_ROW, BTM_ROW)

BOARD = PTS[DEAD]*ROWS*COLS
for j in range(COLS):
  BOARD = change_str(BOARD, coord_to_point(0,   j,COLS), GCH)
  BOARD = change_str(BOARD, coord_to_point(ROWS-1,j,COLS), GCH)
for j in range(ROWS):
  BOARD = change_str(BOARD, coord_to_point(j, 0,   COLS), GCH)
  BOARD = change_str(BOARD, coord_to_point(j, COLS-1,COLS), GCH)

"""
input, output
"""

def char_to_color(c): 
  return PTS.index(c)

escape_ch = '\033['
colorend, textcolor = escape_ch + '0m', escape_ch + '0;37m'
stonecolors = (textcolor, escape_ch + '0;35m', escape_ch + '0;32m')

def showboard(brd, R, C):
  def paint(s):  # s   a string
    pt = ''
    for j in s:
      if j in PTS:      pt += stonecolors[PTS.find(j)] + j + colorend
      elif j.isalnum(): pt += textcolor + j + colorend
      else:             pt += j
    return pt

  pretty = '\n    ' 
  for c in range(C): # columns
    pretty += ' ' + paint(chr(ord('a')+c))
  pretty += '\n'
  for j in range(R): # rows
    if j < 10: pretty += ' '
    pretty += ' ' + paint(str(j)) + ' '
    for k in range(C): # columns
      #print(coord_to_point(j,k,psn.C), end='')
      pretty += ' ' + paint([brd[coord_to_point(j,k,C)]])
    #print('')
    pretty += '\n'
  print(pretty)

def interact():
  itn, psn = 0, BOARD
  while True:
    print('iteration', itn)
    showboard(psn, ROWS, COLS)
    new = copy.copy(psn)
    if new == psn: break
    psn = new

interact()
