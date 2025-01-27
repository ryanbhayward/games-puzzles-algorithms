# simple bfs program to solve sliding tile
from collections import deque
#from random import shuffle
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
      print('')
      
    def targetlist(n): # return target state, as list
      L = []
      for j in range(1,n): L.append(j)
      L.append(0)
      return L
    
    start  = list2str(self.state)
    target = list2str(targetlist(self.rows*self.cols))
    # use a parent dictionary to
    #   - track seen states (all are in dictionary)
    #   - record parents, to recover solution transition sequence
    Parent = { start : start} 
    Fringe = deque() # the sliding tile states, as strings, we encounter
    Fringe.append(start)
    iteration, nodes_this_level, Levels = 0, 1, [1]
    start_time = time()
    while len(Fringe) > 0:
      iteration +=1
      stst = Fringe.popleft() # popleft() and append() give FIFO
      #print(pretty(stst, self.cols, True))
      ndx0 = stst.index('0')
      for shift in self.legal_shifts(ndx0):
        nbr = str_swap(stst,ndx0,shift)
        if nbr == target: 
          print('found target')
          while True:  # show the sequence, backwards
            #sleep(.5)
            print(pretty(stst, self.cols, True))
            p = Parent[stst]
            if p == stst: 
              end_time = time()
              report(iteration, Parent, Levels, end_time-start_time)
              return
            stst = p
        elif nbr not in Parent:
          Parent[nbr] = stst
          Fringe.append(nbr)
      nodes_this_level -= 1
      if nodes_this_level == 0:
        nodes_this_level = len(Fringe)
        Levels.append(nodes_this_level)
        print(' ',iteration,'iterations, level',len(Levels),'has',nodes_this_level,'nodes')
        #sleep(1)
    print('\nno solution found')
    end_time = time()
    report(iteration, Parent, Levels, end_time-start_time)

st = Tile()
st.bfs()
