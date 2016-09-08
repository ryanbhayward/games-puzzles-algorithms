# allows human to play sliding tile  RBH 2016
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

def get_dimensions():
  instr = input('rows columns, e.g. 5 3:  ')
  return int(instr.split()[0]), int(instr.split()[1])

def get_command():
  while True:
    sl = input('< > ^ v ?  ')
    if len(sl)==0: return '\n'
    if sl[0] in '<>^v\n': break
    print('sorry, invalid character')
  return sl[0]

def play():
  r,c = get_dimensions()
  st = Tile(r,c)
  st.showpretty()
  while True:
    ndx0 = st.state.index(min(st.state)) # index of 0
    ch = get_command()
    if ch == '\n': 
      print('\nadios :) \n')
      return
    if ch == '<': #tile goes left, blank goes right
      if st.RT in st.legal_shifts(ndx0): st.slide(st.RT)
      else: print('illegal shift')
    elif ch== '>':
      if st.LF in st.legal_shifts(ndx0): st.slide(st.LF)
      else: print('illegal shift')
    elif ch== '^':
      if st.DN in st.legal_shifts(ndx0): st.slide(st.DN)
      else: print('illegal shift')
    elif ch== 'v':
      if st.UP in st.legal_shifts(ndx0): st.slide(st.UP)
      else: print('illegal shift')
    st.showpretty()

play()
