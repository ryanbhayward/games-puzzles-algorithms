#!/usr/bin/env python3
# simple bfs program to solve sliding tile   rbh 2020
#   - oct 2022: if no solution, print last position seen
# version 2.0 new features
#   - if solution found, give number of moves
#   - unrestricted target (previously target always (1 2 ... n 0) 
#      * user can specify any target position (enter target after start)
#      * if no target entered, then target is (1 2 ... n 0) as usual
#   - after 12 iterations, print all positions on any level 
#       with at most 2 positions (used for assignment 2 solutions)
#   - main loop simplified: check whether current node is target
#       (earlier version checked whether nbr of current is target)

from collections import deque
from time import sleep, time
from sys import stdin

def int2chr(t): # nonneg int to single in '0123456789ABCDEFGHIJ...'
  if t <= 9: return chr(t+ord('0'))
  else:      return chr(t-10 + ord('A'))

def chr2int(c): # chr in '0123456789ABCDEFGHIJ...' to int
  if c in '0123456789': return ord(c) - ord('0')
  else: return 10 + ord(c) - ord('A')

def list2str(L): # list nonneg ints to string monochars
  s = ''
  for x in L: s += int2chr(x)
  return s

def pretty(s,cols,monochar): # string to printable matrix
  # if monochar true: print elements as monochars 
  # else:             print elements as ints
  count, outstr, BLANK = 0, '', ' '
  for x in s:
    count += 1
    if monochar:  
      if x == '0': outstr += ' ' + BLANK
      else:        outstr += ' ' + x
    else:
      if   x == '0':          outstr += '  ' + BLANK     # blank
      elif x in ' 123456789': outstr += '  ' + x         # digit
      else:                   outstr += ' ' + str(chr2int(x))   # 2 digits
    if count%cols == 0: outstr += '\n'
  #sleep(.005)
  return outstr

def str_swap(s,lcn,shift): # swap chars at s[lcn], s[lcn+shift]
  a , b = min(lcn,lcn+shift), max(lcn,lcn+shift)
  return s[:a] + s[b] + s[a+1:b] + s[a] + s[b+1:]

class Tile:
  """a sliding tile class with simple search"""

  def __init__(self):
    # state will be the starting state of any computer search
    # initialized from stdin, 0 is blank, 
    # format: r c then tile entries, row by row, e.g.:
    # 2 3
    # 2 0 5
    # 4 1 3
    self.state = []
    for line in stdin:
      for elem in line.split():
        self.state.append(int(elem))
    # rows, cols are 1st 2 elements of list, so pop them
    self.rows, self.cols = self.state.pop(0), self.state.pop(0)
    # state now holds contents of tile in row-major order
    
    # assert 
    #   - at least 2 rows, at least 2 cols, 
    #   - all entries in [0 .. r*c-1], and
    #   - some entry 0
    assert(self.rows>=2 and self.cols>=2)
    for s in self.state: assert(s>=0 and s < self.rows*self.cols)
    ndx_min = self.state.index(min(self.state))
    assert(self.state[ndx_min] == 0)

    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.cols, self.cols
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down

  def legal_shifts(self,psn): # list of legal shifts
    S = []
    c,r = psn % self.cols, psn // self.cols # column number, row number
    if c > 0:           S.append(self.LF)
    if c < self.cols-1: S.append(self.RT)
    if r > 0:           S.append(self.UP)
    if r < self.rows-1: S.append(self.DN)
    return S

  def bfs(self):
    def report(i, d, L, s):
      print(i,'iterations',s,'seconds',i/s,'itn/s')
      print(len(d), 'states')
      print('nodes by level')
      for j in range(len(L)):  print(j, L[j])
      
    def targetlist(n): # return target state, as list
      L = []
      for j in range(1,n): L.append(j)
      L.append(0)
      return L
    # user must enter the start state ...
    # ... check to see if they also entered a target state
    lenstt, n = len(self.state), self.rows*self.cols
    if lenstt == 2*n:
      start  = list2str(self.state[:n])
      target = list2str(self.state[n:])
    elif lenstt == n:
      start  = list2str(self.state)
      target = list2str(targetlist(n))
    else: assert(False)
    print(start)
    print(target)
    # use a parent dictionary to
    #   - track seen states (all are in dictionary)
    #   - record parents, to recover solution transition sequence
    Parent = { start : start} 
    Fringe = deque() # the sliding tile states (strings) we encounter
    Fringe.append(start)
    iteration, nodes_this_level, Levels = 0, 1, [1]
    start_time = time()
    print('  0 iterations, level 0 has 1 node')
    while len(Fringe) > 0:
      stst = Fringe.popleft() # popleft() and append() give FIFO
      iteration        += 1
      nodes_this_level -= 1
      if stst == target: 
        print('found target,', len(Levels)-1, 'moves')
        while True:
          print(pretty(stst, self.cols, True))
          p = Parent[stst]
          if p == stst:
            end_time = time()
            report(iteration, Parent, Levels, end_time-start_time)
            return
          stst = p
      ndx0 = stst.index('0')
      for shift in self.legal_shifts(ndx0):
        nbr = str_swap(stst,ndx0,shift)
        if nbr not in Parent:
          Parent[nbr] = stst
          Fringe.append(nbr)
      if nodes_this_level == 0:
        nodes_this_level = len(Fringe)
        Levels.append(nodes_this_level)
        print(' ',iteration,'iterations, level',len(Levels),'has',nodes_this_level,'nodes')
        if iteration > 12 and nodes_this_level > 0 and nodes_this_level <= 2:
          for x in Fringe:
            print(pretty(x, self.cols, True))
    print('\nno solution found')
    print('here is the last position encountered:')
    print(pretty(stst, self.cols, True))
    end_time = time()

st = Tile()
st.bfs()
