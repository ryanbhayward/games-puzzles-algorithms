# simple program to solve sliding tile; under construction
from random import shuffle
from time import sleep
from sys import stdin

class Tile:
  """a simple sliding tile class"""

  def __init__(self):
    # state initialized from stdin, 0 is blank, 
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

  def legal_shifts(self,psn):
    S = []
    c,r = psn % self.cols, psn // self.cols # column number, row number
    if c > 0:           S.append(self.LF)
    if c < self.cols-1: S.append(self.RT)
    if r > 0:           S.append(self.UP)
    if r < self.rows-1:      S.append(self.DN)
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
    print(outstring)
    sleep(.5)

st = Tile()
#st.showpretty()
#shuffle(st.state)  # just for testing, not a valid tile operation
st.showpretty()
#uncomment these 2 lines to see verify legal_shifts()
#for j in range(len(st.state)):
#  print(j, st.legal_shifts(j))
ndx0 = st.state.index(min(st.state)) # index of 0
for s in st.legal_shifts(ndx0):
  st.slide(s)
  st.showpretty()
  st.slide(-s)
  st.showpretty()

#for j in range(2):
  #shuffle(st.state)  # just for testing, not a valid tile operation
  #st.showpretty()
  #if ndx0 >= st.
#st.slide(1)
#st.showpretty()
#st.slide(-1)
#st.showpretty()
