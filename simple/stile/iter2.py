# iterative sliding-tile specific algorithm     rbh 2016
# under construction

from random import shuffle
from copy import deepcopy
from time import sleep, time
from sys import stdin

class Tile:
  """a simple sliding tile class"""

  def __init__(self):
    self.state = []
    self.history = []
    for line in stdin:
      for elem in line.split():
        self.state.append(int(elem))
    # rows, cols are 1st 2 elements of list, so pop them
    self.r, self.c = self.state.pop(0), self.state.pop(0)
    # state now holds contents of tile in row-major order

    assert(self.r>=2 and self.c>=2)
    for s in self.state: assert(s>=0 and s < self.r*self.c)
    ndx_min = self.state.index(min(self.state))
    assert(self.state[ndx_min] == 0)

    # these shifts of .state indices effect moves of the blank:
    self.LF, self.RT, self.UP, self.DN = -1, 1, -self.c, self.c
    self.shifts = [self.LF, self.RT, self.UP, self.DN] #left right up down

  def slide(self,shift):
    # slide a tile   shift is from blank's perspective
    b_dx = self.state.index(0) # index of blank
    o_dx = b_dx + shift        # index of other tile
    tmp = deepcopy(self.state)
    tmp[b_dx], tmp[o_dx] = tmp[o_dx], tmp[b_dx]
    if(tmp not in self.history):
      self.state[b_dx], self.state[o_dx] = self.state[o_dx], self.state[b_dx]
      self.history.append(tmp)
    self.showpretty()

  def coords(self,psn): return psn // self.c, psn % self.c
  
  def psn_of(self, coord): return coord[1] + self.c*coord[0]

  def is_UL(self, a_c, b_c): return a_c[0] <= b_c[0] and a_c[1] <= b_c[1]

  def mv_blank(self,psn,direction): # blank to psn, try direction first
    #sleep(.5)
    print('  blank to', psn,'direction',direction,'\n')
    y_crds = self.coords(psn)
    while True:
      b_dx = self.state.index(0)
      if b_dx == psn: return 
      b_crds = self.coords(b_dx)
      if direction==self.LF or direction==self.RT:
        if   b_crds[1] > y_crds[1]: self.slide(self.LF)
        elif b_crds[1] < y_crds[1]: self.slide(self.RT)
        elif b_crds[0] < y_crds[0]: self.slide(self.DN)
        else:                       self.slide(self.UP)
      else: 
        if   b_crds[0] > y_crds[0]: self.slide(self.UP)
        elif b_crds[0] < y_crds[0]: self.slide(self.DN)
        elif b_crds[1] > y_crds[1]: self.slide(self.LF)
        else:                       self.slide(self.RT)

  def blank_ok(self,bc,tc): # blank is left of or above t
    return bc[0]==tc[0] and bc[1]==tc[1]-1 \
        or bc[1]==tc[1] and bc[0]==tc[0]-1

  def showpretty(self):      
    #print(self.rows, self.cols, self.state.index(0), self.shifts)
    count, outstring = 0, ''
    for x in self.state:
      count += 1
      if x==0: outstring   += '   '
      elif x<10: outstring += ' ' + str(x) + ' '
      else: outstring      +=       str(x) + ' '
      if count%self.c == 0: outstring += '\n'
    print(outstring)
    sleep(.5)

  def tst_mv(self):
    r = list(range(self.r*self.c))
    shuffle(r)
    for j in r:
      if j%2==0:
        self.mv_blank(j, self.UP)
      else:
        self.mv_blank(j, self.LF)

  def tst_iter(self):
    #for j in range(10):
    #  print('\ntst',j,'\n')
    #  shuffle(self.state)
    #  sleep(.5)
    #  self.itersolve()
    self.r, self.c = 4, 4
    self.state = [11,10, 9, 2,1,13, 7, 5,15, 0, 8,14,3,12, 6, 4]
    self.itersolve()

  def mv_tile(self, t, dst_index): # move tile t to destination dst_index , destination is index in the array
    def delta_c(ac,bc): return (bc[0]-ac[0],bc[1]-ac[1])

    def init():
      dst_coords = self.coords(dst_index) # destination
      t_index = self.state.index(t)
      t_coords = self.coords(t_index)
      print('dst_index', dst_index, ' t_index', t_index, '\n')
      blank_coords = self.coords(self.state.index(0))
      delta = delta_c(t_coords,dst_coords) # coord delta from tile to dest
      print('                  delta ',delta)
      #sleep(.5)
      abv_t = self.psn_of((t_coords[0]-1,t_coords[1])) # above tile
      left_t  = self.psn_of((t_coords[0],t_coords[1]-1)) # left of tile
      right_t  = self.psn_of((t_coords[0],t_coords[1]+1)) # right of tile
      return dst_coords, t_index, t_coords, blank_coords, delta, abv_t, left_t, right_t

    # assume tiles 1.. t-1 already in psn
    #print('\nmv_tile',t,dst_index,'\n')
    self.showpretty()
    sleep(1)
    self.history = []
    while True:
      dst_coords, t_index, t_coords, blank_coords, delta, abv_t, left_t, right_t = init()
      #print('blank_coords',blank_coords,' t_coords',t_coords,' dst_coords',dst_coords,' abv_t',abv_t,' left_t',left_t,' right_t',right_t)
      if t_index == dst_index: return
      if t_coords[1] < dst_coords[1]: # tile left of destination
        print('tile left dest')
        assert(t_coords[0] > dst_coords[0]) # then tile must also be below
        if t_coords[0]==dst_coords[0]+1: # tile at topmost position
          print('case A')
          if blank_coords[0]<t_coords[0]:
            self.slide(self.DN)
          self.mv_blank(right_t,self.RT)
          self.slide(self.LF)
        elif (blank_coords[1]<t_coords[1] or            # blank left of tile
          blank_coords[1]==t_coords[1] and blank_coords[0]<t_coords[0]): # blank above
          print('case B  abv_t',abv_t)
          self.mv_blank(abv_t,self.UP)
          self.slide(self.DN)
        else: 
          print('case C')
          self.mv_blank(right_t,self.UP)
          self.slide(self.LF)
      # tile not left of destination
      elif t_coords[1]==dst_coords[1]: # tile below dest
        print('tile below dest')
        if t_coords[0]==dst_coords[0]+1:
          print('tile immediately below dest')
          if blank_coords[0]==t_coords[0] and blank_coords[1]<t_coords[1]:
            self.slide(self.DN)
          if blank_coords[0]>=t_coords[0] and blank_coords[1]<=t_coords[1]:
            self.mv_blank(right_t,self.RT)
          self.mv_blank(abv_t,self.UP)
          self.slide(self.DN)
          #print('why not stop here')
        else:
          if blank_coords[1]==t_coords[1] and blank_coords[0]>t_coords[0]:
            self.slide(self.RT)
          self.mv_blank(abv_t,self.UP)
          self.slide(self.DN)
      # tile not left or below
      elif blank_coords[0]>t_coords[0] or blank_coords[0]-blank_coords[1] > t_coords[0]-t_coords[1]:
        # blank below tile or below UL-to-BR diagonal thru tile
        print('tile other dest')
        self.mv_blank(left_t, self.LF)
        self.slide(self.RT)
      elif t_coords[0] == dst_coords[0]: # tile same row as destination
        print('tile other dest')
        if blank_coords[0] == t_coords[0] and blank_coords[1] > t_coords[1]: #blank same row and right
          self.slide(self.DN)
        self.mv_blank(left_t, self.LF)
        self.slide(self.RT)
      else:
        print('tile other dest')
        self.mv_blank(abv_t, self.UP)
        self.slide(self.DN)

      dst_coords, t_index, t_coords, blank_coords, delta, abv_t, left_t, right_t = init()
      if t_index == dst_index: return
      #assert(self.blank_ok(blank_coords,t_coords)) # blank now left or above
      if blank_coords[1]>=dst_coords[1]:
        if blank_coords[0]==t_coords[0] and blank_coords[1]==t_coords[1]-1: self.slide(self.RT)
        if blank_coords[0]==t_coords[0]-1 and blank_coords[1]==t_coords[1]: self.slide(self.DN)
 
  def itersolve(self): # solve iteratively
    def insubboard(xcrd, ulcrd):
      return xcrd[0] >= ulcrd[0] and xcrd[1] >= ulcrd[1]
          
    def shifts(st, lcn, c, L):
      for shift in L:
        st = str_swap(st, lcn, shift)
        lcn += shift
        print(pretty(st, c, True))
      return st

    def finallcn(j): # final position of element j
      return j-1
    
    def col_of(st,cols,c): # in state st, column index of chr c
      return st.index(c) % cols

    def targetlist(n): # return target state, as list
      L = []
      for j in range(1,n): L.append(j)
      L.append(0)
      return L

    UP, DN, LF, RT = self.UP, self.DN, self.LF, self.RT
    self.mv_tile(1,0)
    self.mv_tile(2,1)
    self.mv_tile(3,2)

st = Tile()
#st.tst_mv()
st.tst_iter()
