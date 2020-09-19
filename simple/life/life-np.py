#!/usr/bin/env python3

"""
Conway's game of life, bounded grid, numpy 2-dimensional array rbh 2020
"""

import numpy as np
from time import sleep
from sys import stdin
from paint import paint

PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]

def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""

def live_row(r, B, c): 
  for j in range(c):
    if B[r,j] == ALIVE: return True
  return False

def live_col(c, B, r):
  for k in range(r):
    if B[k,c] == ALIVE: return True
  return False

def alphanum(p, C): #for showing coordinates
  r, c = coord(p, C)
  return 'abcdefghj'[c] + '1234566789'[r]

def get_board(): 
  B = []
  for line in stdin:
    B.append(line.rstrip().replace(' ',''))
  rows, cols = len(B), len(B[0])
  for j in range(1, rows): assert(len(B[j]) == cols)
  return B, rows, cols

def convert_board(B, r, c): # from string to numpy array
  A = np.zeros((r,c), dtype=np.int8)
  for j in range(r):
    for k in range(c):
      if B[j][k]==ACH: A[j,k] = ALIVE
  return A

def expand_grid(A, r, c, t): # add t empty rows and columns on each side
  N = np.zeros((r+2*t,c+2*t), dtype=np.int8)
  for j in range(r):
    for k in range(c):
      if A[j][k]==ALIVE: N[j+t,k+t] = ALIVE
  return N, r+2*t, c+2*t

def print_array(A, r, c): 
  print('')
  for j in range(r):
    out = ''
    for k in range(c):
      out += ACH if A[j,k]==ALIVE else DCH
    print(out)

def show_array(A, r, c):
  for j in range(r):
    line = ''
    for k in range(c):
      line += str(A[j,k])
    print(line)
  print('')

""" 
Conway's next-state formula
"""

def next_state(A, r, c):
  N = np.zeros((r,c), dtype=np.int8)
  changed = False
  for j in range(r):
    for k in range(c):
      num = 0
      if j>0   and k>0   and A[j-1, k-1] == ALIVE: num += 1
      if j>0             and A[j-1, k  ] == ALIVE: num += 1
      if j>0   and k<c-1 and A[j-1, k+1] == ALIVE: num += 1
      if           k>0   and A[j  , k-1] == ALIVE: num += 1
      if j>0   and k<c-1 and A[j  , k+1] == ALIVE: num += 1
      if j<r-1 and k>0   and A[j+1, k-1] == ALIVE: num += 1
      if j<r-1           and A[j+1, k  ] == ALIVE: num += 1
      if j<r-1 and k<c-1 and A[j+1, k+1] == ALIVE: num += 1
      if A[j,k] == ALIVE: 
        if num > 1 and num < 4: 
          N[j,k] = ALIVE
        else:
          N[j,k] = DEAD 
          changed = True
      else:               
        if num == 3:
          N[j,k] = ALIVE
          changed = True
        else:
          N[j,k] = DEAD
  return N, changed

"""
input, output
"""

pause = 0.2

def interact(max_itn):
  itn = 0
  B, r, c = get_board()
  print(B)
  X = convert_board(B,r,c)
  A,r,c = expand_grid(X,r,c,50)
  print_array(A,r,c)
  while itn <= max_itn:
    sleep(pause)
    newA, delta = next_state(A, r, c)
    if not delta:  break
    itn += 1
    A = newA
    print_array(A, r, c)
  print('\niterations', itn)

interact(1000)
