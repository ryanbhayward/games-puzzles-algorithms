#!/usr/bin/env python3
# sliding tile environment   RBH 2016
from random import shuffle

class Tile:
  """a simple sliding tile class"""

  def __init__(self,r,c):
    # state intialized as random permutation
    #   so might not be solvable  :) 
    self.rows, self.cols = r, c
    assert(self.rows>=2 and self.cols>=2)
    self.state = []
    for j in range(r*c): self.state.append(j)
    shuffle(self.state)
    
    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.cols, self.cols
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down
  
  def coord(self,x): return x // self.cols, x % self.cols

  def legal_shifts(self,psn):
    S = []
    c,r = psn % self.cols, psn // self.cols # column number, row number
    if c > 0:           S.append(self.LF)
    if c < self.cols-1: S.append(self.RT)
    if r > 0:           S.append(self.UP)
    if r < self.rows-1: S.append(self.DN)
    return S

  def slide(self,shift):
    # slide a tile   shift is from blank's perspective
    b_dx = self.state.index(0) # index of blank
    o_dx = b_dx + shift        # index of other tile
    self.state[b_dx], self.state[o_dx] = self.state[o_dx], self.state[b_dx]

  def showpretty(self):      
    #print(self.rows, self.cols, self.state.index(0), self.shifts)
    count, outstring = 0, ''
    for x in self.state:
      count += 1
      if x==0: outstring   += '   '
      elif x<10: outstring += ' ' + str(x) + ' '
      else: outstring      +=       str(x) + ' '
      if count%self.cols == 0: outstring += '\n'
    print('\n'+outstring)
    print('inversions', self.inversions(), 
          ' misplaced',self.misplaced(),
          ' taxicab', self.taxicab())

  def taxicab(self):
    total, L, n = 0, self.state, len(self.state)
    for j in range(n):
     if L[j] != 0: 
       final = self.coord(L[j]-1)
       current = self.coord(j)
       for k in range(len(final)):
         total += abs(final[k]-current[k])
    return total

  def inversions(self):
    count, L, n = 0, self.state, len(self.state)
    for x in range(n-1):
      for y in range(x+1,n):
        if L[x] != 0 and L[y] != 0 and L[x] > L[y] : count += 1
    return count

  def misplaced(self):
    count, L, n = 0, self.state, len(self.state)
    for x in range(n):
      if L[x] != 0 and L[x] != x+1: count += 1
    return count

cmd_left = 'd'
cmd_right = 'f'
cmd_up = 'i'
cmd_down = 'j'
cmd_quit = '\n'
cmd_chars = cmd_left + cmd_right + cmd_up + cmd_down + cmd_quit

def get_dimensions():
  instr = input('rows columns, e.g. 5 3:  ')
  return int(instr.split()[0]), int(instr.split()[1])

def get_command():
  while True:
    sl = input('?  slide   < > ^ v   ' 
       + cmd_left + ' ' 
       + cmd_right + ' ' 
       + cmd_up + ' ' 
       + cmd_down + '  ')
    if len(sl)==0: return '\n'
    if sl[0] in cmd_chars: break
    print('sorry, invalid character')
  return sl[0]

def play():
  r,c = get_dimensions()
  #r,c = 3,3
  st = Tile(r,c)
  #st.state = [0,1,2,3,4,5,6,7,8]
  st.showpretty()
  while True:
    ndx0 = st.state.index(min(st.state)) # index of 0
    ch = get_command()
    if ch == cmd_quit: 
      print('\nadios :) \n')
      return
    if ch == cmd_left: #tile goes left, blank goes right
      if st.RT in st.legal_shifts(ndx0): st.slide(st.RT)
      else: print('illegal shift')
    elif ch== cmd_right:
      if st.LF in st.legal_shifts(ndx0): st.slide(st.LF)
      else: print('illegal shift')
    elif ch== cmd_up:
      if st.DN in st.legal_shifts(ndx0): st.slide(st.DN)
      else: print('illegal shift')
    elif ch== cmd_down:
      if st.UP in st.legal_shifts(ndx0): st.slide(st.UP)
      else: print('illegal shift')
    st.showpretty()

play()
