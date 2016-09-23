# iterative sliding-tile specific algorithm     rbh 2016
# under construction

from random import shuffle
from time import sleep, time
from sys import stdin

class Tile:
  """a simple sliding tile class"""

  def __init__(self):
    self.state = []
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
    self.state[b_dx], self.state[o_dx] = self.state[o_dx], self.state[b_dx]
    self.showpretty()

  def coords(self,psn): return psn // self.c, psn % self.c
  
  def psn_of(self, coord): return coord[1] + self.c*coord[0]

  def is_UL(self, a_c, b_c): return a_c[0] <= b_c[0] and a_c[1] <= b_c[1]

  def mv_blank(self,psn,direction): # blank to psn, try direction first
    #sleep(.5)
    #print('  blank to', psn,'direction',direction,'\n')
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
    self.state = [11,10, 9, 2,1,13, 7, 5,15, 0, 8,14,3,12, 6, 4]
    self.itersolve()

  def mv_tile(self,t,xlcn): # move tile t to destination xlcn
    def delta_c(ac,bc): return (bc[0]-ac[0],bc[1]-ac[1])

    def init():
      xc = self.coords(xlcn) # destination
      tlcn = self.state.index(t)
      tc = self.coords(tlcn)
      print('xlcn', xlcn, ' tlcn', tlcn,'\n')
      bc = self.coords(self.state.index(0))
      delta = delta_c(tc,xc) # coord delta from tile to dest
      #print('                  delta ',delta)
      #sleep(.5)
      abv = self.psn_of((tc[0]-1,tc[1])) # above tile
      lf  = self.psn_of((tc[0],tc[1]-1)) # left of tile
      rt  = self.psn_of((tc[0],tc[1]+1)) # right of tile
      return xc, tlcn, tc, bc, delta, abv, lf, rt

    # assume tiles 1.. t-1 already in psn
    #print('\nmv_tile',t,xlcn,'\n')
    self.showpretty()
    sleep(1)
    while True:
      xc, tlcn, tc, bc, delta, abv, lf, rt = init()
      #print('bc',bc,' tc',tc,' xc',xc,' abv',abv,' lf',lf,' rt',rt)
      if tlcn == xlcn: return
      if tc[1] < xc[1]: # tile left of destination
        print('tile left dest')
        assert(tc[0] > xc[0]) # then tile must also be below
        if tc[0]==xc[0]+1: # tile at topmost position
          print('case A')
          if bc[0]<tc[0]:
            self.slide(self.DN)
          self.mv_blank(rt,self.RT)
          self.slide(self.LF)
        elif (bc[1]<tc[1] or            # blank left of tile 
          bc[1]==tc[1] and bc[0]<tc[0]): # blank above
          print('case B  abv',abv)
          self.mv_blank(abv,self.UP)
          self.slide(self.DN)
        else: 
          print('case C')
          self.mv_blank(rt,self.UP) 
          self.slide(self.LF)
      # tile not left of destination
      elif tc[1]==xc[1]: # tile below dest
        #print('tile below dest')
        if tc[0]==xc[0]+1: 
          #print('tile immediately below dest')
          if bc[0]==tc[0] and bc[1]<tc[1]: 
            self.slide(self.DN)
          if bc[0]>=tc[0] and bc[1]<=tc[1]: 
            self.mv_blank(rt,self.RT)
          self.mv_blank(abv,self.UP)
          self.slide(self.DN)
          #print('why not stop here')
        else:
          if bc[1]==tc[1] and bc[0]>tc[0]:
            self.slide(self.RT)
          self.mv_blank(abv,self.UP)
          self.slide(self.DN)
      # tile not left or below
      elif bc[0]>tc[0] or bc[0]-bc[1] > tc[0]-tc[1]: 
        # blank below tile or below UL-to-BR diagonal thru tile
        #print('tile other dest')
        self.mv_blank(lf, self.LF)
        self.slide(self.RT)
      elif tc[0] == xc[0]: # tile same row as destination
        #print('tile other dest')
        if bc[0] == tc[0] and bc[1] > tc[1]: #blank same row and right
          self.slide(self.DN)
        self.mv_blank(lf, self.LF)
        self.slide(self.RT)
      else:
        #print('tile other dest')
        self.mv_blank(abv, self.UP)
        self.slide(self.DN)

      xc, tlcn, tc, bc, delta, abv, lf, rt = init()
      if tlcn == xlcn: return
      #assert(self.blank_ok(bc,tc)) # blank now left or above
      if bc[1]>=xc[1]:
        if bc[0]==tc[0] and bc[1]==tc[1]-1: self.slide(self.RT)
        if bc[0]==tc[0]-1 and bc[1]==tc[1]: self.slide(self.DN)
 
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
